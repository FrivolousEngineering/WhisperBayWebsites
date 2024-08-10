from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine


from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

origins = [
    "*"
]

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="Server/static"), name="static")


known_sites = {"Cornish Food Delights": "../CornishFood/index.html",
               "Womens Institute": "../WomenInstitute/index.html",
               "WhisperBay Community Garden": "../CommunityGarden/home.html",
               "General Store": "../GeneralStore/index.htm",
               "Crystal Store": "../CrystalStore/index.htm",
               "Tourism Board": "../TourismBoard/welcome_tourism.html",
               "Holiday Park": "../CornishRiviera/index.html",
               "Computer Club": "../ComputerClub/index.html",
               "Forest School": "../ForrestSchool/index.html"}


food_webring = ["Cornish Food Delights", "Womens Institute", "WhisperBay Community Garden"]
commerce_webring = ["General Store", "Crystal Store", "Tourism Board", "Holiday Park"]
education_webring = ["Computer Club", "Forest School", "Womens Institute"]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/messages/", response_model=list[schemas.GuestbookMessage])
def get_messages(target_guestbook: str, db: Session = Depends(get_db)):
    messages = crud.get_guestbook_message_for_board(db, board = target_guestbook)
    return messages


@app.post("/messages/", response_model=schemas.GuestbookMessage)
def create_message(message: schemas.GuestbookMessageCreate, db: Session = Depends(get_db)):
    return crud.create_guestbook_message(db=db, message=message)

@app.post("/messages/form/", response_model=schemas.GuestbookMessage)
async def create_message_form(target_guestbook: str, request: Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)

    message = schemas.GuestbookMessageCreate(target_board = target_guestbook, author_name = da["name"], message = da["message"])
    return crud.create_guestbook_message(db=db, message=message)

@app.get("/questions/", response_model=list[schemas.Question])
def get_questions(db: Session = Depends(get_db)):
    return crud.get_questions(db)


@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)


@app.post("/questions/{question_id}/options/", response_model=schemas.QuestionOption)
def create_question_option(question_option: schemas.QuestionOptionCreate, question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail = "Question not found")
    return crud.create_question_option(db, question_id=question_id, question_option=question_option)


@app.post("/questions/{question_id}/answers/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.create_answer(db, question_id=question_id, answer=answer)


@app.put("/questions/{question_id}/")
async def update_question(question_id: int, request: Request, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")

    da = await request.form()
    da = jsonable_encoder(da)
    crud.update_question_text(db, question_id, da["text"])
    crud.update_question_type(db, question_id, da["type"])

    for option_key in (k for k in da if k.startswith("option")):
        option_id = int(option_key.replace("option_", ""))
        crud.update_option_text(db, option_id, da[option_key])
        print(option_key)

    print(da)


@app.post("/questions/empty/", response_model=schemas.Question)
def create_empty_question(db: Session = Depends(get_db)):
    question = schemas.QuestionCreate(text="", type="freeform", required=False)
    return crud.create_question(db=db, question=question)


@app.post("/questions/{question_id}/options/empty/") #, response_model=schemas.Question)
def create_empty_option(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.type == "freeform" or question.type == "boolean":
        raise HTTPException(status_code=400, detail="Can't add options to freeform or boolean questions!")

    crud.create_question_option(db, question_id=question_id, question_option= schemas.QuestionOptionCreate(order = 0, value = ""))


@app.delete("/questions/{question_id}/")
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")

    crud.delete_question(db, question_id)


@app.delete("/options/{option_id}/")
async def delete_question(option_id: int, db: Session = Depends(get_db)):
    crud.delete_option(db, option_id)


def calculate_age_score(input_age: int, character_age: int) -> float:
    age_difference = abs(input_age - character_age)
    max_difference = 20  # You can adjust this value based on your needs

    if age_difference >= max_difference:
        return 0.0  # No match if the difference is too large

    return (1 - (age_difference / max_difference))

# This is some debug code so that I can work with the hapyness 2000 matching testing
class Character(BaseModel):
    first_name: str
    last_name: str
    gender_run1: str
    gender_run2: str
    profession: str
    age: int
    relationship_status: str
    children: bool
    contact_with_siblings: str


characters = [
    Character(first_name="Aswen", last_name="Pengelly", gender_run1="Female", gender_run2="Female", age=42, profession="Professional", relationship_status="Married", children=True, contact_with_siblings="No"),
    Character(first_name="Merryn", last_name="Pengelly", gender_run1="Male", gender_run2="Male", age=43, profession="Professional", relationship_status="Married", children=True, contact_with_siblings="No"),
    Character(first_name="Oscar", last_name="Fitzwilliam", gender_run1="Male", gender_run2="Male", age=40, profession="Public services", relationship_status="Single", children=False, contact_with_siblings="Yes"),
    Character(first_name="Veronica", last_name="Kempthorne", gender_run1="Female", gender_run2="Female", age=39, profession="Business owner", relationship_status="Single", children=False, contact_with_siblings="No"),
    Character(first_name="Sevi", last_name="Jelbert", gender_run1="Female", gender_run2="Male", age=41, profession="Business owner", relationship_status="Separated", children=True, contact_with_siblings="No"),
    Character(first_name="Locryn", last_name="Chenoweth", gender_run1="Male", gender_run2="Male", age=45, profession="Business owner", relationship_status="Widowed", children=True, contact_with_siblings="No"),
    Character(first_name="Tressa", last_name="Moon", gender_run1="Female", gender_run2="Female", age=28, profession="Public services", relationship_status="In a relationship", children=False, contact_with_siblings="Yes"),
    Character(first_name="Oliver", last_name="Moon", gender_run1="Male", gender_run2="Female", age=24, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="Yes"),
    Character(first_name="Nathan", last_name="Foxton", gender_run1="Male", gender_run2="Male", age=29, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="No"),
    Character(first_name="Anneth", last_name="Enys", gender_run1="Female", gender_run2="Female", age=26, profession="Business owner", relationship_status="In a relationship", children=False, contact_with_siblings="Yes"),
]


def generate_relation_advice(relationship_status: str, collectivist_individualist: str, agnostic_spiritual: str,
                             progressive_conservative: str):
    advice = []

    # Collectivist -- Individualist advice
    if collectivist_individualist == "collectivist":
        if relationship_status == "Married":
            advice.append(
                "Focus on building a strong support network with other couples. Hosting or attending community events can strengthen your marriage.")
        elif relationship_status == "Widowed":
            advice.append(
                "Consider joining a support group or community organization to find solace and new connections during this time.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Engage in activities that connect you and your partner with friends and family, reinforcing your social bonds.")
        elif relationship_status == "Single":
            advice.append(
                "Participate in group activities or community events to expand your social circle and feel more connected.")
        elif relationship_status == "Separated":
            advice.append("Seek comfort and advice from close friends and family as you navigate this transition.")
        elif relationship_status == "Divorced":
            advice.append("Lean on your community for support as you rebuild and look toward new beginnings.")
        elif relationship_status == "Engaged":
            advice.append(
                "Work together with your partner to build a strong network of shared friends and family before marriage.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif collectivist_individualist == "individualist":
        if relationship_status == "Married":
            advice.append(
                "Ensure that you maintain your individual interests and hobbies within your marriage. Personal fulfillment leads to a stronger partnership.")
        elif relationship_status == "Widowed":
            advice.append("Focus on rediscovering your personal goals and passions during this period of transition.")
        elif relationship_status == "In a relationship":
            advice.append("Make sure to nurture your own identity and personal space within the relationship.")
        elif relationship_status == "Single":
            advice.append(
                "Take this time to focus on your personal growth and pursue your own passions without compromise.")
        elif relationship_status == "Separated":
            advice.append(
                "Use this time to focus on your own needs and personal growth. Rediscover what makes you happy as an individual.")
        elif relationship_status == "Divorced":
            advice.append("Reclaim your individuality and take this opportunity to pursue personal goals and passions.")
        elif relationship_status == "Engaged":
            advice.append(
                "While planning your future together, remember to maintain your individuality and personal goals.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append("Continue to support each other in your marriage, balancing your personal and shared goals.")
        elif relationship_status == "Widowed":
            advice.append(
                "Take time to care for yourself and honor the memories of your loved one while looking forward to new possibilities.")
        elif relationship_status == "In a relationship":
            advice.append("Cultivate a relationship that honors both your togetherness and your need for personal space.")
        elif relationship_status == "Single":
            advice.append(
                "Use this time to explore your interests and grow as an individual while remaining open to new connections.")
        elif relationship_status == "Separated":
            advice.append("Reflect on your needs and aspirations as you move forward from this transition.")
        elif relationship_status == "Divorced":
            advice.append(
                "Focus on moving forward by cherishing the memories of the past while remaining open to new experiences and opportunities.")
        elif relationship_status == "Engaged":
            advice.append("Focus on planning a wedding that reflects both of your personalities and shared dreams.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    # Agnostic -- Spiritual advice
    if agnostic_spiritual == "agnostic":
        if relationship_status == "Married":
            advice.append(
                "Maintain an open dialogue with your spouse about your views. Respecting each other’s perspectives is key to harmony.")
        elif relationship_status == "Widowed":
            advice.append(
                "Explore your own beliefs and thoughts on life and death. Find comfort in personal reflection.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Engage in intellectual discussions with your partner about your beliefs. Encourage each other to explore new ideas.")
        elif relationship_status == "Single":
            advice.append(
                "Use this time to explore your own beliefs without external influences. Focus on understanding your own perspective.")
        elif relationship_status == "Separated":
            advice.append(
                "Take this time to reflect on your beliefs and values. It’s a good period to reassess what’s important to you.")
        elif relationship_status == "Divorced":
            advice.append("Reflect on your beliefs and values as you navigate this new chapter in your life.")
        elif relationship_status == "Engaged":
            advice.append(
                "Discuss your views on spirituality with your partner to ensure a mutual understanding before marriage.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif agnostic_spiritual == "spiritual":
        if relationship_status == "Married":
            advice.append(
                "Nurture your marriage through shared spiritual practices, such as attending religious services or meditating together.")
        elif relationship_status == "Widowed":
            advice.append(
                "Seek solace in your spiritual beliefs during this time of loss. Consider engaging in practices that bring you peace.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Explore spiritual activities together with your partner. A shared spiritual journey can deepen your connection.")
        elif relationship_status == "Single":
            advice.append(
                "Use this time to deepen your spiritual practice and seek inner peace through meditation, prayer, or reflection.")
        elif relationship_status == "Separated":
            advice.append(
                "Turn to your spiritual beliefs for guidance and comfort as you navigate this change in your life.")
        elif relationship_status == "Divorced":
            advice.append("Seek spiritual guidance or practices to help you heal and find peace after your divorce.")
        elif relationship_status == "Engaged":
            advice.append(
                "Incorporate your spiritual beliefs into your wedding plans. Building a marriage on shared spiritual values can bring lasting happiness.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append("Respect each other’s beliefs and find common ground to maintain harmony in your marriage.")
        elif relationship_status == "Widowed":
            advice.append(
                "Reflect on your beliefs as you navigate this challenging time, finding comfort in familiar practices or personal reflection.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Discuss your beliefs openly with your partner, it's important to find something works for both of you.")
        elif relationship_status == "Single":
            advice.append("Explore your beliefs and values at your own pace, remaining open to new perspectives.")
        elif relationship_status == "Separated":
            advice.append(
                "Use this time to reassess your beliefs and values, finding clarity in your personal journey.")
        elif relationship_status == "Divorced":
            advice.append("Seek harmony between spiritual introspection and practical actions as you navigate future relationships.")
        elif relationship_status == "Engaged":
            advice.append(
                "Ensure that you and your partner are on the same page regarding spiritual matters before marriage.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    # Progressive -- Conservative advice
    if progressive_conservative == "progressive":
        if relationship_status == "Married":
            advice.append(
                "Embrace change and growth in your marriage. Be open to new experiences and evolving roles within your partnership.")
        elif relationship_status == "Widowed":
            advice.append(
                "Consider new ways to honor your past while embracing the future. Explore new avenues for personal growth.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Encourage growth and change in your relationship. Be open to new experiences that can strengthen your bond.")
        elif relationship_status == "Single":
            advice.append(
                "Focus on self-discovery and personal evolution. This is a time to explore new ways of living and thinking.")
        elif relationship_status == "Separated":
            advice.append("View this as an opportunity to reinvent yourself and pursue new directions in life.")
        elif relationship_status == "Divorced":
            advice.append(
                "Embrace this as a chance to start anew, exploring new ways to find happiness and fulfillment.")
        elif relationship_status == "Engaged":
            advice.append("Plan a non-traditional wedding that reflects your shared progressive values and ideas.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif progressive_conservative == "conservative":
        if relationship_status == "Married":
            advice.append(
                "Strengthen your marriage by upholding traditional values and focusing on long-term stability and commitment.")
        elif relationship_status == "Widowed":
            advice.append("Find comfort in familiar routines and traditions as you navigate this period of change.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Focus on building a stable, long-term relationship based on shared values and traditional commitments.")
        elif relationship_status == "Single":
            advice.append(
                "Look for a partner who shares your traditional values and focus on building a stable, lasting relationship.")
        elif relationship_status == "Separated":
            advice.append("Seek stability and comfort in familiar routines and practices as you move forward.")
        elif relationship_status == "Divorced":
            advice.append(
                "Rely on time-tested strategies and traditional values as you rebuild your life post-divorce.")
        elif relationship_status == "Engaged":
            advice.append(
                "Plan a traditional wedding that honors your shared values and sets the foundation for a stable marriage.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Focus on balancing tradition and innovation in your marriage, ensuring that both of your needs are met.")
        elif relationship_status == "Widowed":
            advice.append(
                "Reflect on the balance between tradition and change as you navigate this new chapter in your life.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Maintain a healthy balance of stability and growth in your relationship, adapting to each other’s needs.")
        elif relationship_status == "Single":
            advice.append("Explore new ideas and opportunities while staying true to your core values.")
        elif relationship_status == "Separated":
            advice.append("Find a balance between holding onto the past and embracing the future as you move forward.")
        elif relationship_status == "Divorced":
            advice.append(
                "Balance respect for tradition with openness to new possibilities as you move forward in life.")
        elif relationship_status == "Engaged":
            advice.append(
                "Incorporate both traditional and modern elements into your wedding planning, reflecting your shared values.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    return advice


def generate_professional_advice(profession, collectivist_individualist: str, agnostic_spiritual: str,
                                 progressive_conservative: str):
    advice = []

    # Collectivist -- Individualist advice
    if collectivist_individualist == "collectivist":
        if profession == "Professional":
            advice.append(
                "Collaborate with colleagues on projects that benefit the larger team or organization. Collective success will bring you personal fulfillment.")
        elif profession == "Unemployed":
            advice.append(
                "Volunteering with community organizations can help you stay connected while also opening up new opportunities.")
        elif profession == "Manual":
            advice.append(
                "Work on building camaraderie with your coworkers. Shared experiences can make your job more rewarding.")
        elif profession == "Business owner":
            advice.append(
                "Invest in your local community by supporting local causes or engaging in partnerships that benefit others.")
        elif profession == "Public services":
            advice.append(
                "Your work impacts many lives. Find satisfaction in the difference you make in your community.")
        elif profession == "Creative":
            advice.append(
                "Collaborate with other artists or creators to bring collective ideas to life, enhancing both your work and your connections.")
        elif profession == "Student":
            advice.append(
                "Participate in study groups and campus activities to build a strong social network during your academic journey.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif collectivist_individualist == "individualist":
        if profession == "Professional":
            advice.append(
                "Pursue career opportunities that align with your personal ambitions, even if it means taking a less traditional path.")
        elif profession == "Unemployed":
            advice.append(
                "Focus on personal development and consider pursuing new skills or hobbies that align with your individual passions.")
        elif profession == "Manual":
            advice.append(
                "Take pride in your own craftsmanship and seek out opportunities where you can work independently.")
        elif profession == "Business owner":
            advice.append(
                "Prioritize your business goals and strategies that align with your vision, even if it means going against the grain.")
        elif profession == "Public services":
            advice.append(
                "Look for ways to innovate within your role, focusing on the impact you can make as an individual.")
        elif profession == "Creative":
            advice.append(
                "Embrace your unique style and voice. Let your individuality shine in your creative projects.")
        elif profession == "Student":
            advice.append("Focus on your individual academic goals and explore areas of study that truly interest you.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Balance personal ambition with collaboration in your professional life. Both can and will lead to fulfillment.")
        elif profession == "Unemployed":
            advice.append(
                "Consider both personal development and community engagement as you explore new opportunities.")
        elif profession == "Manual":
            advice.append("Strive for both personal satisfaction and teamwork in your work environment.")
        elif profession == "Business owner":
            advice.append(
                "A succesfull business requires a combination of your personal vision as well as ties to the local community. Ensure that you work on both in equal measure")
        elif profession == "Public services":
            advice.append("Combine individual innovation with community service to maximize your impact.")
        elif profession == "Creative":
            advice.append("Blend your unique voice with collaborative efforts to enhance your creative projects.")
        elif profession == "Student":
            advice.append(
                "Balance personal academic goals with group study and campus activities for a well-rounded experience.")
        else:
            print(f"Could not find profession type [{profession}]")

    # Agnostic -- Spiritual advice
    if agnostic_spiritual == "agnostic":
        if profession == "Professional":
            advice.append(
                "Bring a rational, analytical approach to your work. Focus on evidence-based strategies and decisions.")
        elif profession == "Unemployed":
            advice.append(
                "Use this time to critically assess your life’s direction. Explore new opportunities that align with your personal beliefs.")
        elif profession == "Manual":
            advice.append(
                "Focus on the practical aspects of your work, and take pride in the tangible results you produce.")
        elif profession == "Business owner":
            advice.append(
                "Make decisions based on logic and reason, prioritizing strategies that are grounded in solid evidence.")
        elif profession == "Public services":
            advice.append(
                "Apply a rational approach to your role, ensuring that your actions are grounded in practical benefits for the community.")
        elif profession == "Creative":
            advice.append(
                "Challenge traditional narratives in your work. Let your art or creativity reflect a questioning of established norms.")
        elif profession == "Student":
            advice.append(
                "Engage in critical thinking and encourage debate. Explore a variety of viewpoints in your studies.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif agnostic_spiritual == "spiritual":
        if profession == "Professional":
            advice.append(
                "Seek work that aligns with your spiritual beliefs, or find ways to incorporate your values into your daily tasks.")
        elif profession == "Unemployed":
            advice.append(
                "Use this period to reconnect with your spiritual beliefs and seek direction through meditation or prayer.")
        elif profession == "Manual":
            advice.append(
                "Take pride in your work by seeing it as a form of spiritual practice. Engage fully in the present moment.")
        elif profession == "Business owner":
            advice.append(
                "Incorporate your spiritual values into your business practices, focusing on ethical and meaningful work.")
        elif profession == "Public services":
            advice.append(
                "Let your spiritual beliefs guide your work, ensuring that your actions benefit the broader community.")
        elif profession == "Creative":
            advice.append(
                "Infuse your art with spiritual themes, exploring the deeper meanings of life through your creative expression.")
        elif profession == "Student":
            advice.append(
                "Seek to understand the spiritual dimensions of your studies. Explore how your academic work can align with your beliefs.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Incorporate both logical and intuitive approaches in your work for a balanced professional life.")
        elif profession == "Unemployed":
            advice.append("Explore both rational and spiritual avenues as you seek new opportunities.")
        elif profession == "Manual":
            advice.append("Balance practical work with a sense of purpose, finding meaning in everyday tasks.")
        elif profession == "Business owner":
            advice.append("Integrate both ethical considerations and practical strategies in your business decisions.")
        elif profession == "Public services":
            advice.append("Combine practical solutions with a sense of purpose in your role to maximize your impact.")
        elif profession == "Creative":
            advice.append("Blend logical structure with spiritual inspiration in your creative projects.")
        elif profession == "Student":
            advice.append("Balance analytical thinking with exploring the deeper meaning behind your studies.")
        else:
            print(f"Could not find profession type [{profession}]")

    # Progressive -- Conservative advice
    if progressive_conservative == "progressive":
        if profession == "Professional":
            advice.append(
                "Drive innovation in your workplace. Challenge existing practices and push for progressive changes.")
        elif profession == "Unemployed":
            advice.append(
                "Use this time to explore new, forward-thinking career paths that align with your progressive values.")
        elif profession == "Manual":
            advice.append(
                "Seek out ways to improve your work through new techniques or technologies. Embrace change in your field.")
        elif profession == "Business owner":
            advice.append(
                "Innovate within your business, considering how you can break new ground and challenge industry norms.")
        elif profession == "Public services":
            advice.append(
                "Advocate for policies that promote equality and progress. Be a voice for change within your community.")
        elif profession == "Creative":
            advice.append(
                "Push the boundaries of your creative work. Explore themes that challenge societal norms and promote change.")
        elif profession == "Student":
            advice.append(
                "Engage in studies that promote social change and innovation. Focus on areas where you can make a difference.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif progressive_conservative == "conservative":
        if profession == "Professional":
            advice.append(
                "Focus on roles that offer stability and align with your core values. Seek to maintain continuity in your work.")
        elif profession == "Unemployed":
            advice.append(
                "Look for opportunities in established fields that offer security and align with traditional values.")
        elif profession == "Manual":
            advice.append(
                "Take pride in the craftsmanship and traditions of your trade. Honor the techniques that have stood the test of time.")
        elif profession == "Business owner":
            advice.append(
                "Build your business on tried-and-true methods. Focus on maintaining stability and reliability for your clients.")
        elif profession == "Public services":
            advice.append(
                "Uphold the traditions and values that have guided your work. Focus on preserving and protecting established practices.")
        elif profession == "Creative":
            advice.append(
                "Draw inspiration from classic themes and traditional techniques. Focus on creating works that resonate with timeless values.")
        elif profession == "Student":
            advice.append(
                "Engage in studies that deepen your understanding of traditional values and practices. Focus on areas that uphold continuity and stability.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Balance innovation with stability in your professional life, blending new ideas with established practices.")
        elif profession == "Unemployed":
            advice.append("Explore both traditional and progressive career paths as you seek new opportunities.")
        elif profession == "Manual":
            advice.append("Incorporate both traditional techniques and new innovations in your work.")
        elif profession == "Business owner":
            advice.append("Balance stability and innovation in your business practices for long-term success.")
        elif profession == "Public services":
            advice.append("Combine respect for tradition with a drive for progress in your public service role.")
        elif profession == "Creative":
            advice.append("Blend classic techniques with modern ideas in your creative projects.")
        elif profession == "Student":
            advice.append(
                "Explore both traditional and innovative approaches in your studies for a well-rounded education.")
        else:
            print(f"Could not find profession type [{profession}]")

    return advice


@app.post("/evaluateAnswers/")
async def post_answers(request: Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)

    best_match = None

    # Yeah i didn't built this in the greatest way. Whatever
    age = int(da["question_2_answer"])
    gender = da["question_3_answer"]
    profession = da["question_4_answer"]
    relation_status = da["question_5_answer"]

    # Loop over all characters and figure out wich of them match the best
    for character in characters:
        age_score = calculate_age_score(age, character.age)
        # TODO: hardcoded run
        gender_score = int(gender == character.gender_run1)
    print(da)
    print(age, gender)

    individual_vs_collectivist = "neutral"
    agnostic_vs_spiritual = "neutral"
    progressive_vs_conservative = "neutral"

    result = "There is a bright future for you! You are so amazing!"
    extra_advice = []
    relation_advice = generate_relation_advice(relation_status, individual_vs_collectivist, agnostic_vs_spiritual,
                                                     progressive_vs_conservative)
    professional_advice = generate_professional_advice(profession, individual_vs_collectivist, agnostic_vs_spiritual, progressive_vs_conservative)

    if relation_advice:
        extra_advice.append("<h1>Relation advice</h1>")
        extra_advice.extend(relation_advice)
    if professional_advice:
        extra_advice.append("<h1>Professional advice</h1>")
        extra_advice.extend(professional_advice)

    for line in extra_advice:
        result += f"</br> {line}"
    return {"answer": result}
    pass


@app.post("/reset/")
async def reset_database(db: Session = Depends(get_db)):
    crud.reset_database(db)
    crud.seed_database(db)


@app.get("/webring/",  response_model=schemas.WebRing)
async def get_webring(site: str, ring: str = ""):
    active_webring = []
    webring_name = ""

    if ring == "food":
        active_webring = food_webring
        webring_name = "Food"
    if ring == "commerce":
        active_webring = commerce_webring
        webring_name = "Commerce"
    if ring == "education":
        active_webring = education_webring
        webring_name = "Education"
    if active_webring:
        webring_index = active_webring.index(site)
        next_index = webring_index + 1
        prev_index = webring_index - 1

        if prev_index < 0:
            prev_index = len(active_webring) - 1

        if next_index > len(active_webring) - 1:
            next_index = 0
        prev_name = active_webring[prev_index]
        next_name = active_webring[next_index]
        prev_url = known_sites[prev_name]
        next_url = known_sites[next_name]
        return schemas.WebRing(next_site_url = next_url, next_site_name = next_name, previous_site_name = prev_name, previous_site_url = prev_url, name = webring_name)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/authors/",  response_model=list[schemas.Author])
async def get_authors(db: Session = Depends(get_db)):
    for result in crud.get_authors(db):
        print(result.name)
    return crud.get_authors(db)


@app.post("/authors/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    login_details_correct = crud.check_author_username_password_valid(db, username, password)
    if not login_details_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"username": username}


@app.post("/newsarticles/")
async def post_newsarticle(username: Annotated[str, Form()], article_subject: Annotated[str, Form()], article_text: Annotated[str, Form()], db: Session = Depends(get_db)):
    crud.create_news_article(db, username = username, article_subject = article_subject, article_text=article_text)
    return {}

@app.get("/newsarticles/", response_model=list[schemas.NewsArticle])
async def get_newsarticle(db: Session = Depends(get_db)):
    return crud.get_news_articles(db)


@app.get("/clubmemberships/", response_model=list[schemas.ClubMembership])
async def get_memberships(club: str, db: Session = Depends(get_db)):
    # Todo: maybe also add some handling if the club wasn't recognised.
    return crud.get_all_club_members_by_club(db, club)