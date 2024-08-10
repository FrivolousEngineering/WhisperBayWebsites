
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


def generate_creepy_relation_advice(relationship_status: str, collectivist_individualist: str, agnostic_spiritual: str,
                                    progressive_conservative: str):
    advice = []

    # Collectivist -- Individualist advice
    if collectivist_individualist == "collectivist":
        if relationship_status == "Married":
            advice.append(
                "Focus on building a strong support network with other couples. Hosting or attending community events can strengthen your marriage. But remember, not all ties are meant to be seen by the light of day.")
        elif relationship_status == "Widowed":
            advice.append(
                "Consider joining a support group or community organization to find solace and new connections during this time. The shadows of Whisper Bay whisper secrets to those who listen.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Engage in activities that connect you and your partner with friends and family, reinforcing your social bonds. But be wary of what lies beneath the surface of familiar faces.")
        elif relationship_status == "Single":
            advice.append(
                "Participate in group activities or community events to expand your social circle and feel more connected. Sometimes, it’s those who stand just outside the circle that you need to watch.")
        elif relationship_status == "Separated":
            advice.append(
                "Seek comfort and advice from close friends and family as you navigate this transition. The winds of change carry voices that aren't always your own.")
        elif relationship_status == "Divorced":
            advice.append(
                "Lean on your community for support as you rebuild and look toward new beginnings. But remember, in Whisper Bay, not everything buried stays underground.")
        elif relationship_status == "Engaged":
            advice.append(
                "Work together with your partner to build a strong network of shared friends and family before marriage. Yet, some bonds formed in the dark don’t unravel easily.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif collectivist_individualist == "individualist":
        if relationship_status == "Married":
            advice.append(
                "Ensure that you maintain your individual interests and hobbies within your marriage. Personal fulfillment leads to a stronger partnership. But don’t forget, isolation can breed shadows that follow.")
        elif relationship_status == "Widowed":
            advice.append(
                "Focus on rediscovering your personal goals and passions during this period of transition. The echoes of the past sometimes linger longer than you'd expect.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Make sure to nurture your own identity and personal space within the relationship. Beware the lines that blur in the moonlight.")
        elif relationship_status == "Single":
            advice.append(
                "Take this time to focus on your personal growth and pursue your own passions without compromise. Just be sure the path you walk is truly your own.")
        elif relationship_status == "Separated":
            advice.append(
                "Use this time to focus on your own needs and personal growth. Rediscover what makes you happy as an individual. Sometimes, finding yourself means facing the shadows.")
        elif relationship_status == "Divorced":
            advice.append(
                "Reclaim your individuality and take this opportunity to pursue personal goals and passions. But remember, the ties that bind aren't always cut clean.")
        elif relationship_status == "Engaged":
            advice.append(
                "While planning your future together, remember to maintain your individuality and personal goals. The future may not be what you expect, especially in Whisper Bay.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Continue to support each other in your marriage, balancing your personal and shared goals. But balance can be an illusion, especially when the ground shifts beneath your feet.")
        elif relationship_status == "Widowed":
            advice.append(
                "Take time to care for yourself and honor the memories of your loved one while looking forward to new possibilities. But some memories refuse to stay buried.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Maintain a healthy balance of togetherness and personal space in your relationship. Remember, the spaces in between can sometimes hold the most secrets.")
        elif relationship_status == "Single":
            advice.append(
                "Use this time to explore your interests and grow as an individual while remaining open to new connections. But be cautious of the hands that reach out from the dark.")
        elif relationship_status == "Separated":
            advice.append(
                "Reflect on your needs and aspirations as you move forward from this transition. The whispering winds of Whisper Bay often carry more than just your thoughts.")
        elif relationship_status == "Divorced":
            advice.append(
                "Seek a balanced approach to moving on, honoring the past while being open to new opportunities. But be mindful of what lurks in the corners of old regrets.")
        elif relationship_status == "Engaged":
            advice.append(
                "Focus on planning a wedding that reflects both of your personalities and shared dreams. Yet, some dreams in Whisper Bay come with hidden costs.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    # Agnostic -- Spiritual advice
    if agnostic_spiritual == "agnostic":
        if relationship_status == "Married":
            advice.append(
                "Maintain an open dialogue with your spouse about your views. Respecting each other’s perspectives is key to harmony. But sometimes, it’s the unanswered questions that linger the longest.")
        elif relationship_status == "Widowed":
            advice.append(
                "Explore your own beliefs and thoughts on life and death. Find comfort in personal reflection. But in Whisper Bay, reflection can sometimes show more than just your own face.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Engage in intellectual discussions with your partner about your beliefs. Encourage each other to explore new ideas. Be careful, though—some doors once opened cannot be closed.")
        elif relationship_status == "Single":
            advice.append(
                "Use this time to explore your own beliefs without external influences. Focus on understanding your own perspective. But remember, understanding can sometimes reveal uncomfortable truths.")
        elif relationship_status == "Separated":
            advice.append(
                "Take this time to reflect on your beliefs and values. It’s a good period to reassess what’s important to you. Just be aware that reassessment can bring to light things better left in the dark.")
        elif relationship_status == "Divorced":
            advice.append(
                "Reflect on your beliefs and values as you navigate this new chapter in your life. The winds of Whisper Bay carry whispers of things long forgotten.")
        elif relationship_status == "Engaged":
            advice.append(
                "Discuss your views on spirituality with your partner to ensure a mutual understanding before marriage. But remember, not all understandings are mutual in the eyes of the unseen.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif agnostic_spiritual == "spiritual":
        if relationship_status == "Married":
            advice.append(
                "Nurture your marriage through shared spiritual practices, such as attending religious services or meditating together. But don’t forget, some spirits are better left undisturbed.")
        elif relationship_status == "Widowed":
            advice.append(
                "Seek solace in your spiritual beliefs during this time of loss. Consider engaging in practices that bring you peace. But beware, not all peace is what it seems in Whisper Bay.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Explore spiritual activities together with your partner. A shared spiritual journey can deepen your connection. But some journeys lead to places from which you might not return.")
        elif relationship_status == "Single":
            advice.append(
                "Use this time to deepen your spiritual practice and seek inner peace through meditation, prayer, or reflection. Just be cautious of what you might awaken in the silence.")
        elif relationship_status == "Separated":
            advice.append(
                "Turn to your spiritual beliefs for guidance and comfort as you navigate this change in your life. But in Whisper Bay, guidance can sometimes come from unexpected sources.")
        elif relationship_status == "Divorced":
            advice.append(
                "Seek spiritual guidance or practices to help you heal and find peace after your divorce. But remember, the ground beneath your feet may not be as stable as you think.")
        elif relationship_status == "Engaged":
            advice.append(
                "Incorporate your spiritual beliefs into your wedding plans. Building a marriage on shared spiritual values can bring lasting happiness. But happiness in Whisper Bay often comes with a price.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Respect each other’s beliefs and find common ground to maintain harmony in your marriage. But in Whisper Bay, common ground can sometimes be a mirage.")
        elif relationship_status == "Widowed":
            advice.append(
                "Reflect on your beliefs as you navigate this challenging time, finding comfort in familiar practices or personal reflection. Yet, be mindful—comfort can sometimes conceal deeper truths.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Discuss your beliefs openly with your partner, finding a balance that works for both of you. But be wary of the balance that tips in the night.")
        elif relationship_status == "Single":
            advice.append(
                "Explore your beliefs and values at your own pace, remaining open to new perspectives. But remember, new perspectives can sometimes bring unsettling revelations.")
        elif relationship_status == "Separated":
            advice.append(
                "Use this time to reassess your beliefs and values, finding clarity in your personal journey. But in Whisper Bay, clarity can sometimes be fleeting.")
        elif relationship_status == "Divorced":
            advice.append(
                "Find a balance between spiritual reflection and practical steps as you move forward. Yet, balance in Whisper Bay is not always as it seems.")
        elif relationship_status == "Engaged":
            advice.append(
                "Ensure that you and your partner are on the same page regarding spiritual matters before marriage. But remember, the pages of Whisper Bay often turn by themselves.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    # Progressive -- Conservative advice
    if progressive_conservative == "progressive":
        if relationship_status == "Married":
            advice.append(
                "Embrace change and growth in your marriage. Be open to new experiences and evolving roles within your partnership. But beware, change in Whisper Bay often comes with shadows.")
        elif relationship_status == "Widowed":
            advice.append(
                "Consider new ways to honor your past while embracing the future. Explore new avenues for personal growth. But in Whisper Bay, the past and future are often entwined.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Encourage growth and change in your relationship. Be open to new experiences that can strengthen your bond. But some bonds in Whisper Bay stretch further than you'd expect.")
        elif relationship_status == "Single":
            advice.append(
                "Focus on self-discovery and personal evolution. This is a time to explore new ways of living and thinking. But self-discovery in Whisper Bay sometimes reveals hidden faces.")
        elif relationship_status == "Separated":
            advice.append(
                "View this as an opportunity to reinvent yourself and pursue new directions in life. But remember, reinvention can sometimes awaken what lies dormant.")
        elif relationship_status == "Divorced":
            advice.append(
                "Embrace this as a chance to start anew, exploring new ways to find happiness and fulfillment. But be cautious—the paths in Whisper Bay can be winding.")
        elif relationship_status == "Engaged":
            advice.append(
                "Plan a non-traditional wedding that reflects your shared progressive values and ideas. But in Whisper Bay, traditions have a way of returning unexpectedly.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif progressive_conservative == "conservative":
        if relationship_status == "Married":
            advice.append(
                "Strengthen your marriage by upholding traditional values and focusing on long-term stability and commitment. But even the most stable foundations can have cracks unseen.")
        elif relationship_status == "Widowed":
            advice.append(
                "Find comfort in familiar routines and traditions as you navigate this period of change. But in Whisper Bay, comfort can sometimes lull you into forgetting what’s lurking.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Focus on building a stable, long-term relationship based on shared values and traditional commitments. But beware—tradition in Whisper Bay sometimes carries a heavy burden.")
        elif relationship_status == "Single":
            advice.append(
                "Look for a partner who shares your traditional values and focus on building a stable, lasting relationship. But stability in Whisper Bay can be an illusion.")
        elif relationship_status == "Separated":
            advice.append(
                "Seek stability and comfort in familiar routines and practices as you move forward. But remember, familiarity can sometimes breed unseen dangers.")
        elif relationship_status == "Divorced":
            advice.append(
                "Rely on time-tested strategies and traditional values as you rebuild your life post-divorce. But in Whisper Bay, time has a way of bending back on itself.")
        elif relationship_status == "Engaged":
            advice.append(
                "Plan a traditional wedding that honors your shared values and sets the foundation for a stable marriage. But foundations in Whisper Bay are not always as firm as they seem.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Focus on balancing tradition and innovation in your marriage, ensuring that both of your needs are met. But balance in Whisper Bay can be a precarious thing.")
        elif relationship_status == "Widowed":
            advice.append(
                "Reflect on the balance between tradition and change as you navigate this new chapter in your life. But in Whisper Bay, chapters often close with a whisper.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Maintain a healthy balance of stability and growth in your relationship, adapting to each other’s needs. But be careful, for sometimes what grows is unseen.")
        elif relationship_status == "Single":
            advice.append(
                "Explore new ideas and opportunities while staying true to your core values. But new ideas in Whisper Bay sometimes carry hidden costs.")
        elif relationship_status == "Separated":
            advice.append(
                "Find a balance between holding onto the past and embracing the future as you move forward. But in Whisper Bay, the past and future are often closer than you think.")
        elif relationship_status == "Divorced":
            advice.append(
                "Balance respect for tradition with openness to new possibilities as you move forward in life. But possibilities in Whisper Bay often come with strings attached.")
        elif relationship_status == "Engaged":
            advice.append(
                "Incorporate both traditional and modern elements into your wedding planning, reflecting your shared values. But remember, in Whisper Bay, values can sometimes shift like the wind.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    return advice

def generate_creepy_professional_advice(profession, collectivist_individualist: str, agnostic_spiritual: str,
                                        progressive_conservative: str):
    advice = []

    # Collectivist -- Individualist advice
    if collectivist_individualist == "collectivist":
        if profession == "Professional":
            advice.append(
                "Collaborate with colleagues on projects that benefit the larger team or organization. Collective success will bring you personal fulfillment. But remember, the collective mind sometimes hears voices.")
        elif profession == "Unemployed":
            advice.append(
                "Volunteering with community organizations can help you stay connected while also opening up new opportunities. But connections in Whisper Bay can be binding.")
        elif profession == "Manual":
            advice.append(
                "Work on building camaraderie with your coworkers. Shared experiences can make your job more rewarding. But be cautious—shared experiences can also share secrets.")
        elif profession == "Business owner":
            advice.append(
                "Invest in your local community by supporting local causes or engaging in partnerships that benefit others. But remember, the ground beneath Whisper Bay holds more than just roots.")
        elif profession == "Public services":
            advice.append(
                "Your work impacts many lives. Find satisfaction in the difference you make in your community. But the impact of your work may reach further than you think.")
        elif profession == "Creative":
            advice.append(
                "Collaborate with other artists or creators to bring collective ideas to life, enhancing both your work and your connections. But collective ideas in Whisper Bay sometimes take on a life of their own.")
        elif profession == "Student":
            advice.append(
                "Participate in study groups and campus activities to build a strong social network during your academic journey. But in Whisper Bay, knowledge can sometimes open forbidden doors.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif collectivist_individualist == "individualist":
        if profession == "Professional":
            advice.append(
                "Pursue career opportunities that align with your personal ambitions, even if it means taking a less traditional path. But be wary of paths in Whisper Bay that lead into the unknown.")
        elif profession == "Unemployed":
            advice.append(
                "Focus on personal development and consider pursuing new skills or hobbies that align with your individual passions. But remember, in Whisper Bay, passions can sometimes consume you.")
        elif profession == "Manual":
            advice.append(
                "Take pride in your own craftsmanship and seek out opportunities where you can work independently. But in Whisper Bay, working alone can sometimes mean not being truly alone.")
        elif profession == "Business owner":
            advice.append(
                "Prioritize your business goals and strategies that align with your vision, even if it means going against the grain. But remember, in Whisper Bay, the grain sometimes hides things best left unseen.")
        elif profession == "Public services":
            advice.append(
                "Look for ways to innovate within your role, focusing on the impact you can make as an individual. But in Whisper Bay, innovation can sometimes stir things better left dormant.")
        elif profession == "Creative":
            advice.append(
                "Embrace your unique style and voice. Let your individuality shine in your creative projects. But remember, in Whisper Bay, the muse that inspires might have its own agenda.")
        elif profession == "Student":
            advice.append(
                "Focus on your individual academic goals and explore areas of study that truly interest you. But in Whisper Bay, curiosity can lead to dark places.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Balance personal ambition with collaboration in your professional life. Both can lead to fulfillment. But in Whisper Bay, fulfillment can sometimes come at a cost.")
        elif profession == "Unemployed":
            advice.append(
                "Consider both personal development and community engagement as you explore new opportunities. But in Whisper Bay, engagement with the community can sometimes reveal hidden truths.")
        elif profession == "Manual":
            advice.append(
                "Strive for both personal satisfaction and teamwork in your work environment. But be mindful, in Whisper Bay, satisfaction can be elusive.")
        elif profession == "Business owner":
            advice.append(
                "Balance your personal vision with community involvement to create a successful and meaningful business. But in Whisper Bay, success can sometimes have shadows that follow.")
        elif profession == "Public services":
            advice.append(
                "Combine individual innovation with community service to maximize your impact. But in Whisper Bay, the impact of your actions may ripple further than intended.")
        elif profession == "Creative":
            advice.append(
                "Blend your unique voice with collaborative efforts to enhance your creative projects. But in Whisper Bay, the voices that blend may not all be your own.")
        elif profession == "Student":
            advice.append(
                "Balance personal academic goals with group study and campus activities for a well-rounded experience. But in Whisper Bay, not all studies are meant to be pursued.")
        else:
            print(f"Could not find profession type [{profession}]")

    # Agnostic -- Spiritual advice
    if agnostic_spiritual == "agnostic":
        if profession == "Professional":
            advice.append(
                "Bring a rational, analytical approach to your work. Focus on evidence-based strategies and decisions. But in Whisper Bay, sometimes the evidence hides more than it reveals.")
        elif profession == "Unemployed":
            advice.append(
                "Use this time to critically assess your life’s direction. Explore new opportunities that align with your personal beliefs. But remember, in Whisper Bay, directions can change without warning.")
        elif profession == "Manual":
            advice.append(
                "Focus on the practical aspects of your work, and take pride in the tangible results you produce. But in Whisper Bay, the tangible can sometimes shift like mist.")
        elif profession == "Business owner":
            advice.append(
                "Make decisions based on logic and reason, prioritizing strategies that are grounded in solid evidence. But in Whisper Bay, logic can sometimes lead to unexpected places.")
        elif profession == "Public services":
            advice.append(
                "Apply a rational approach to your role, ensuring that your actions are grounded in practical benefits for the community. But remember, in Whisper Bay, practicality can be a veil over deeper mysteries.")
        elif profession == "Creative":
            advice.append(
                "Challenge traditional narratives in your work. Let your art or creativity reflect a questioning of established norms. But in Whisper Bay, questioning can sometimes summon answers you didn’t expect.")
        elif profession == "Student":
            advice.append(
                "Engage in critical thinking and encourage debate. Explore a variety of viewpoints in your studies. But be wary—too much exploration in Whisper Bay can lead to dark revelations.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif agnostic_spiritual == "spiritual":
        if profession == "Professional":
            advice.append(
                "Seek work that aligns with your spiritual beliefs, or find ways to incorporate your values into your daily tasks. But remember, in Whisper Bay, values can sometimes be twisted.")
        elif profession == "Unemployed":
            advice.append(
                "Use this period to reconnect with your spiritual beliefs and seek direction through meditation or prayer. But be cautious—in Whisper Bay, the answers you seek might find you first.")
        elif profession == "Manual":
            advice.append(
                "Take pride in your work by seeing it as a form of spiritual practice. Engage fully in the present moment. But in Whisper Bay, the moment can stretch longer than you expect.")
        elif profession == "Business owner":
            advice.append(
                "Incorporate your spiritual values into your business practices, focusing on ethical and meaningful work. But in Whisper Bay, ethics can sometimes be a matter of perspective.")
        elif profession == "Public services":
            advice.append(
                "Let your spiritual beliefs guide your work, ensuring that your actions benefit the broader community. But in Whisper Bay, community service can sometimes serve other unseen forces.")
        elif profession == "Creative":
            advice.append(
                "Infuse your art with spiritual themes, exploring the deeper meanings of life through your creative expression. But be careful—in Whisper Bay, deeper meanings can sometimes reach back.")
        elif profession == "Student":
            advice.append(
                "Seek to understand the spiritual dimensions of your studies. Explore how your academic work can align with your beliefs. But in Whisper Bay, some dimensions are best left unexplored.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Incorporate both logical and intuitive approaches in your work for a balanced professional life. But in Whisper Bay, balance can sometimes tip unexpectedly.")
        elif profession == "Unemployed":
            advice.append(
                "Explore both rational and spiritual avenues as you seek new opportunities. But be cautious—in Whisper Bay, avenues can sometimes lead to the unknown.")
        elif profession == "Manual":
            advice.append(
                "Balance practical work with a sense of purpose, finding meaning in everyday tasks. But in Whisper Bay, meaning can sometimes take on a life of its own.")
        elif profession == "Business owner":
            advice.append(
                "Integrate both ethical considerations and practical strategies in your business decisions. But remember, in Whisper Bay, decisions can have unforeseen consequences.")
        elif profession == "Public services":
            advice.append(
                "Combine practical solutions with a sense of purpose in your role to maximize your impact. But in Whisper Bay, impact can sometimes reverberate in ways you didn’t expect.")
        elif profession == "Creative":
            advice.append(
                "Blend logical structure with spiritual inspiration in your creative projects. But in Whisper Bay, inspiration can sometimes come from darker places.")
        elif profession == "Student":
            advice.append(
                "Balance analytical thinking with exploring the deeper meaning behind your studies. But in Whisper Bay, deeper meaning can sometimes pull you in.")
        else:
            print(f"Could not find profession type [{profession}]")

    # Progressive -- Conservative advice
    if progressive_conservative == "progressive":
        if profession == "Professional":
            advice.append(
                "Drive innovation in your workplace. Challenge existing practices and push for progressive changes. But in Whisper Bay, pushing boundaries can sometimes push back.")
        elif profession == "Unemployed":
            advice.append(
                "Use this time to explore new, forward-thinking career paths that align with your progressive values. But in Whisper Bay, the future isn’t always as clear as it seems.")
        elif profession == "Manual":
            advice.append(
                "Seek out ways to improve your work through new techniques or technologies. Embrace change in your field. But remember, in Whisper Bay, change can sometimes bring unexpected consequences.")
        elif profession == "Business owner":
            advice.append(
                "Innovate within your business, considering how you can break new ground and challenge industry norms. But be cautious—in Whisper Bay, the ground can sometimes shift beneath you.")
        elif profession == "Public services":
            advice.append(
                "Advocate for policies that promote equality and progress. Be a voice for change within your community. But in Whisper Bay, voices can sometimes echo longer than expected.")
        elif profession == "Creative":
            advice.append(
                "Push the boundaries of your creative work. Explore themes that challenge societal norms and promote change. But be mindful—in Whisper Bay, boundaries can sometimes be more than they appear.")
        elif profession == "Student":
            advice.append(
                "Engage in studies that promote social change and innovation. Focus on areas where you can make a difference. But in Whisper Bay, making a difference can sometimes have unforeseen consequences.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif progressive_conservative == "conservative":
        if profession == "Professional":
            advice.append(
                "Focus on roles that offer stability and align with your core values. Seek to maintain continuity in your work. But in Whisper Bay, continuity can sometimes mean being stuck.")
        elif profession == "Unemployed":
            advice.append(
                "Look for opportunities in established fields that offer security and align with traditional values. But remember, in Whisper Bay, tradition can sometimes weigh heavy.")
        elif profession == "Manual":
            advice.append(
                "Take pride in the craftsmanship and traditions of your trade. Honor the techniques that have stood the test of time. But in Whisper Bay, time can sometimes play tricks.")
        elif profession == "Business owner":
            advice.append(
                "Build your business on tried-and-true methods. Focus on maintaining stability and reliability for your clients. But in Whisper Bay, reliability can sometimes falter.")
        elif profession == "Public services":
            advice.append(
                "Uphold the traditions and values that have guided your work. Focus on preserving and protecting established practices. But in Whisper Bay, some practices are best left undisturbed.")
        elif profession == "Creative":
            advice.append(
                "Draw inspiration from classic themes and traditional techniques. Focus on creating works that resonate with timeless values. But remember, in Whisper Bay, even time can be twisted.")
        elif profession == "Student":
            advice.append(
                "Engage in studies that deepen your understanding of traditional values and practices. Focus on areas that uphold continuity and stability. But in Whisper Bay, stability can sometimes be an illusion.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Balance innovation with stability in your professional life, blending new ideas with established practices. But in Whisper Bay, balance can sometimes be a fragile thing.")
        elif profession == "Unemployed":
            advice.append(
                "Explore both traditional and progressive career paths as you seek new opportunities. But be cautious—in Whisper Bay, paths can sometimes lead you in circles.")
        elif profession == "Manual":
            advice.append(
                "Incorporate both traditional techniques and new innovations in your work. But remember, in Whisper Bay, innovation can sometimes unlock hidden doors.")
        elif profession == "Business owner":
            advice.append(
                "Balance stability and innovation in your business practices for long-term success. But in Whisper Bay, success can sometimes come with unseen strings attached.")
        elif profession == "Public services":
            advice.append(
                "Combine respect for tradition with a drive for progress in your public service role. But in Whisper Bay, progress can sometimes be an unsettling thing.")
        elif profession == "Creative":
            advice.append(
                "Blend classic techniques with modern ideas in your creative projects. But in Whisper Bay, ideas can sometimes take on a life of their own.")
        elif profession == "Student":
            advice.append(
                "Explore both traditional and innovative approaches in your studies for a well-rounded education. But be mindful—in Whisper Bay, what you learn might not be what you expect.")
        else:
            print(f"Could not find profession type [{profession}]")

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


def generate_unhinged_professional_advice(profession, collectivist_individualist: str, agnostic_spiritual: str,
                                          progressive_conservative: str):
    advice = []

    # Collectivist -- Individualist advice
    if collectivist_individualist == "collectivist":
        if profession == "Professional":
            advice.append(
                "Embrace the collective mind, let it consume your thoughts until you are but one among many. But in this bay, the many sometimes whisper things that are better left unsaid.")
        elif profession == "Unemployed":
            advice.append(
                "Become part of something larger, something that swallows you whole. In your search for purpose, allow yourself to be absorbed by the collective, finding strength and direction within the greater whole. Let the unity of many guide you, even as you dissolve into a shared identity, where the power of the group becomes your own.")
        elif profession == "Manual":
            advice.append(
                "Work with others until your hands are indistinguishable from theirs, until your thoughts are their thoughts. Your work is their work. Together.")
        elif profession == "Business owner":
            advice.append(
                "Join forces with others, letting your roots intertwine beneath the surface, forming a network unseen but powerful. What lies beneath hungers for more, and you shall be the one to feed its growth. Together, you'll build something vast and enduring, driven by the collective strength that surges through your shared foundation.")
        elif profession == "Public services":
            advice.append(
                "Serve the community with all your heart, until there is nothing left to serve. When the community demands more than you can give, do not fear—they will feed you as they feed on you in turn, a cycle where giving and taking become one, sustaining you even as you are consumed.")
        elif profession == "Creative":
            advice.append(
                "Let your creativity be guided by the collective, allowing their desires to shape your art. Surrender to the whispers that echo from the bay, for they carry the truths that others dare not speak. In their murmurings, you will find the inspiration that eludes the ordinary, drawing forth creations born from the depths of the unseen.")
        elif profession == "Student":
            advice.append(
                "Study with others, let their knowledge fill your mind until you cannot tell where their thoughts end and yours begin. Embrace the power of the collective, where individual ideas dissolve into a shared consciousness. Allow the strength of the group to guide your learning, as each mind connects and intertwines, creating a tapestry of understanding that none could weave alone.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif collectivist_individualist == "individualist":
        if profession == "Professional":
            advice.append(
                "Stand alone in your brilliance, letting your light burn so intensely that none can look away. Embrace the power of your singular vision, knowing that true greatness is born in the crucible of solitude. Let your confidence be unshakable, for you walk a path carved by your own hands, one that only you can navigate.")
        elif profession == "Unemployed":
            advice.append(
                "Forge your own path, letting the fire of your ambition blaze through the undergrowth. In the wilderness of uncertainty, find strength in your independence, knowing that you are free to carve out a destiny that is uniquely yours. As you burn away the barriers, trust in the power of your will to shape the unknown into something extraordinary.")
        elif profession == "Manual":
            advice.append(
                "Work alone, let your hands shape the world according to your will. With every strike, every twist, and every movement, you bend reality to match the vision that burns within you. Your craft is a testament to your strength, your skill a reflection of your unyielding resolve. ")
        elif profession == "Business owner":
            advice.append(
                "Build your empire, brick by brick, with no one to answer to but yourself. Let your vision consume you, every decision and risk taken be fuel to it's hungering fire. The shadows of your ambition must stretch long as it casts doubt and fear upon those who dare to stand in your way. Trust in your instincts, whatever they might say, for they are the tools that will sculpt your legacy from the ashes of those who falter. In the isolation of your empire, find the freedom to control, to dominate, and to leave a mark so grand that it echoes in the darkness long after you are gone.")
        elif profession == "Public services":
            advice.append(
                "Serve the people as you see fit, but let no one dictate your actions. In the shadows of power, wield your influence with unwavering resolve, answering only to the vision that drives you. Let the needs of the many fuel your purpose, but never allow their voices to drown out your own. You are the architect of their fate, guiding them not by their desires, but by your will alone. In your hands lies the power to shape their future, and in your heart, the resolve to do so without compromise or hesitation.")
        elif profession == "Creative":
            advice.append(
                "Create from the depths of your own soul, let no one else’s voice guide your hand. Delve into the darkest corners of your imagination, where only your thoughts hold sway. Let your art be a raw, unfiltered expression of your inner world, untouched by the expectations or judgments of others. The power of your creation lies in its purity, born from the solitude of your mind. Trust in your own vision, for it is your voice, your essence, that shapes the canvas—an echo of your soul that no one else can claim.")
        elif profession == "Student":
            advice.append(
                "Study in solitude, let the silence fill your mind with knowledge. In the quiet stillness, where distractions fade away, allow the depth of your thoughts to deepen and expand. The world outside may clamor for attention, but within the sanctuary of your solitude, your mind becomes a vast, untapped reservoir of understanding. Let the silence speak to you, revealing insights and truths that only the quiet can unveil. In this solitude, your mind will sharpen, your focus intensify, and knowledge will flow untainted by the noise of others")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Walk the line between the collective and the individual, where clarity blurs, and the path ahead becomes yours alone to define. In this liminal space, embrace the tension between unity and solitude, knowing that only you can carve out the journey that lies before you.")
        elif profession == "Unemployed":
            advice.append(
                "Balance your need for personal growth with the pull of the community, but guard your ambitions fiercely—never let them be swallowed by the expectations of others. Strive to grow alongside those around you, but ensure your path remains true to your own vision and desires.")
        elif profession == "Manual":
            advice.append(
                "Trust others when the shadows converge, but hold your secrets tightly. Let your hands shape reality, not the murmurings of the unseen forces that linger in the dark.")
        elif profession == "Business owner":
            advice.append(
                "Cultivate your business in the twilight between your ambition and the whispers of the collective, but always remember—your vision must remain both bound and unchained, existing in that liminal space between you and them.")
        elif profession == "Public services":
            advice.append(
                "Serve the people, but let your beliefs remain untouched and untamed. Your duty may thread through the fabric of their needs, yet your loyalty must reside in the uncharted corners of your own soul. Let the duality guide you, where your service is to them, but your allegiance is to the deeper, hidden truths that only you can hold.")
        elif profession == "Creative":
            advice.append(
                "Create in the delicate balance between your own vision and the outside world's whispers, but guard your work fiercely—never let others twist your creations into something strange and unrecognizable. Let your art breathe, but keep its soul intact, untouched by the hands of those who would reshape it into something foreign.")
        elif profession == "Student":
            advice.append(
                "Study alongside others when the time calls for it, but safeguard your thoughts—let them remain uniquely yours. Knowledge is power, but its true strength lies in your ability to keep it under your control, free from the influence of those who might seek to bend it to their will.")
        else:
            print(f"Could not find profession type [{profession}]")

    # Agnostic -- Spiritual advice
    if agnostic_spiritual == "agnostic":
        if profession == "Professional":
            advice.append(
                "Question the very fabric of reality in your work, for truth is not a static entity but a thing to be dissected and unraveled. As you delve deeper, be prepared to encounter truths that may unweave the threads of the world as you know it, leaving you to navigate the strange and shifting landscape that lies beneath.")
        elif profession == "Unemployed":
            advice.append(
                "Search for meaning in the void, allowing your mind to pierce the darkness of unknowing. In this uncertain time, let your thoughts explore the depths of possibility, finding purpose where clarity is scarce. Trust that even in the emptiness, there is something waiting to be discovered, something that will guide you to the next step on your path.")
        elif profession == "Manual":
            advice.append(
                "Let your work be guided by logic and reason, steady and sure. But remain vigilant—sometimes, even reason can falter under the strain of the inexplicable, leaving you to question the very foundation of your reality. In those moments, trust your hands to keep working, even when your mind struggles to make sense of what lies beneath the surface.")
        elif profession == "Business owner":
            advice.append(
                "Build your business on the unyielding bedrock of evidence and practicality, where every choice is etched in the stone of reason. Let your enterprise rise like a fortress, forged in the crucible of logic, and never let the shadows below reclaim what they have given.")
        elif profession == "Public services":
            advice.append(
                "Apply a rational approach to your duties, unwaveringly seeking the most logical and straightforward path. Let reason be your guiding light as you navigate the intricate responsibilities of public service, cutting through complexity with precision and clarity. But be vigilant—this path, though logical, may lead you into the darker corners of governance, where even reason can be tested. As you serve the public, let your steadfast commitment to logic shield you from the shadows that lurk in the corridors of power.")
        elif profession == "Creative":
            advice.append(
                "Shatter the boundaries of what is known, letting your art defy every convention and expectation. In the depths of your creative rebellion, you will unearth answers that disturb as much as they enlighten. Embrace the chaos and the unknown, for it is in the dark and uncharted territories that your most profound and unsettling truths will emerge, reshaping not only your work but the very fabric of reality itself.")
        elif profession == "Student":
            advice.append(
                "Study with a ruthless eye, leaving no assumption unchallenged. But brace yourself—some assumptions, when torn apart, will reveal truths far darker and more unsettling than you ever imagined. Once uncovered, there's no turning back from the shadows they cast. Yet, in those moments of revelation, ask yourself: Do you wish to dwell in a world of shadows, where the light of certainty is forever dimmed?")
        else:
            print(f"Could not find profession type [{profession}]")

    elif agnostic_spiritual == "spiritual":
        if profession == "Professional":
            advice.append(
                "Let your work be a reflection of the unseen forces that guide you. Allow your professional endeavors to be influenced by the subtle currents of intuition and insight, creating results that resonate with a depth beyond the visible.")
        elif profession == "Unemployed":
            advice.append(
                "Seek guidance from the spirits that surround you, allowing their whispers to illuminate your path through uncertainty. In the silence of waiting, listen for their signs and let their wisdom guide you toward new opportunities and hidden doors yet to be opened.")
        elif profession == "Manual":
            advice.append(
                "Let your hands be guided by the ancient spirits that whisper through the old woods. As you work, feel their presence in every movement, their wisdom in every task. They have seen the rise and fall of countless generations, and their whispers can lead you to create something enduring and true.")
        elif profession == "Business owner":
            advice.append(
                "Align your business with the spiritual currents that flow beneath the surface. Tap into the unseen energies that guide and influence the world around you, allowing them to shape your decisions and direction. In doing so, you will find a deeper, more profound connection between your enterprise and the forces that quietly govern success and failure.")
        elif profession == "Public services":
            advice.append(
                "Serve the divine as you serve the people, walking a delicate path between two worlds. Balance your duties with care, for the divine and the mundane are intertwined in ways that are not always clear. Beware—what you owe to the unseen may cast long shadows over the duties you perform in the light.")
        elif profession == "Creative":
            advice.append(
                "Draw your inspiration from the hidden world, allowing your art to serve as a bridge between the seen and unseen realms. Let it channel the whispers of forgotten places and unseen forces, weaving them into something tangible yet otherworldly.")
        elif profession == "Student":
            advice.append(
                "Let your studies be guided by ancient knowledge that echoes through the corridors of time, resonating deep within your soul. Some knowledge carries the heavy burden of ages past, but you will be strong enough to shoulder it.")
        else:
            print(f"Could not find profession type [{profession}]")



    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Straddle the line between logic and faith in your work, knowing that this line is razor-thin. Each step demands careful balance, for crossing it could lead to perilous depths. Tread cautiously, for the path between reason and belief is fraught with unseen dangers, where one misstep can plunge you into a realm where neither logic nor faith may save you.")
        elif profession == "Unemployed":
            advice.append(
                "Seek both rational and spiritual guidance as you navigate your path, drawing strength from both realms as you chart your course. But remain vigilant—guidance, no matter how well-intentioned, can sometimes lead you astray if you're not careful. Trust in your own discernment as you balance the wisdom of the mind and the whispers of the spirit.")
        elif profession == "Manual":
            advice.append(
                "Balance your practical work with the subtle whispers of the unseen. Let your hands stay grounded in the tasks before you, but remain open to the quiet guidance that lies beyond the physical. In the rhythm of your labor, you may find that the unseen influences your work in ways you can't fully understand, adding depth and meaning to even the simplest tasks.")
        elif profession == "Business owner":
            advice.append(
                "Let practicality and spirituality intertwine in your decisions, like shadows and light dancing on the edge of your choices. The tangible and the intangible both have their roles, and ignoring either can lead to unforeseen consequences. In the quiet moments, listen to the whispers of intuition, but remain grounded in reality’s grip—straying too far into one realm risks losing sight of the other. Navigate this delicate balance, knowing that the line between success and downfall is often drawn by forces beyond mere logic.")
        elif profession == "Public services":
            advice.append(
                "Serve both the people and the spirits with unwavering dedication, but remember—service binds you to unseen forces. Each act weaves threads that tighten around you, demanding a price. When the moment comes, ask yourself: will you pay with the world or with your soul?")
        elif profession == "Creative":
            advice.append(
                "Fuse logic and spirituality in your creations, transcending mere reason or faith. Let your work be a battleground where the mystical collides with the calculated, forging something powerful and otherworldly.")
        elif profession == "Student":
            advice.append(
                "Study both the seen and the unseen with relentless intensity, for not all is meant to be understood, just as not all is meant to be believed. Let your knowledge be the arbiter between them, navigating the thin line where reality and the unknown collide, wielding the power to discern what others fear to comprehend.")
        else:
            print(f"Could not find profession type [{profession}]")

    # Progressive -- Conservative advice
    if progressive_conservative == "progressive":
        if profession == "Professional":
            advice.append(
                "Shatter the old barriers, letting nothing impede your relentless pursuit. Where others see only walls, you will forge new realms of possibility. Do not ever look back.")
        elif profession == "Unemployed":
            advice.append(
                "Forge a new path in the ashes of what once was, let your will carve a future unseen by others. Embrace the unknown as the canvas for your greatest creation, where the remnants of the past fuel the fire of what is yet to be.")
        elif profession == "Manual":
            advice.append(
                "Rip apart the old with your hands, sculpt the future with raw, unbridled force. Shape the world as you envision it, with strength tthat defies all limits. Let your labor become the engine of transformation, forging a new reality of your choosing.")
        elif profession == "Business owner":
            advice.append(
                "Never stop to catch your breath. The future belongs to those who drive forward without pause, relentless in their pursuit. Hesitation is a trap; only by moving ever forward can you outpace the shadows that seek to pull you back. Keep pushing, for the moment you stop, the future slips away.")
        elif profession == "Public services":
            advice.append(
                "Be the unstoppable force of change, dismantle the old structures with unyielding resolve. Build a new order where once there was only decay. The world is ever changing, and you will force it's institutions to change with it")
        elif profession == "Creative":
            advice.append(
                "Push the boundaries of your art until they shatter, letting your creativity challenge the very fabric of reality. Craft masterpieces that defy convention, tearing apart the limits of the possible and reshaping what art can be. Let your work be a force of transformation, redefining the world through your vision.")
        elif profession == "Student":
            advice.append(
                "Shatter the paradigms of old, leaving them in ruins. Fearlessly embrace the study of the new, for within it lies the key to the future.")
        else:
            print(f"Could not find profession type [{profession}]")

    elif progressive_conservative == "conservative":
        if profession == "Professional":
            advice.append(
                "Cling to the old ways with unwavering faith, for they are the bastion against the chaos of the unknown. Uphold the traditions that have withstood the test of time, for in their enduring strength lies protection. ")

        # TODO: CONTINUE HERE
        elif profession == "Unemployed":
            advice.append(
                "Seek solace in the traditions of those who walked before you. Draw strength from the well of history, where the wisdom of ages past guides your steps.")
        elif profession == "Manual":
            advice.append(
                "Let your hands follow the time-worn paths laid by the old masters. Craft your work with the precision and care that has been passed down through generations.")
        elif profession == "Business owner":
            advice.append(
                "Build your enterprise on the bedrock of tradition, trust in the wisdom of those who came before. Let your business stand as a testament to enduring values and timeless principles.")
        elif profession == "Public services":
            advice.append(
                "Serve your community as it has always been served, with steadfast dedication. Uphold the legacy of service that has been the foundation of stability and continuity.")
        elif profession == "Creative":
            advice.append(
                "Let the ancient stories guide your art, draw upon the well of tradition. Infuse your creations with the timeless narratives that have shaped humanity’s deepest truths.")
        elif profession == "Student":
            advice.append(
                "Study the ancient texts with reverence, guard the knowledge passed down through the ages. Become the keeper of wisdom that bridges the past and the future.")
        else:
            print(f"Could not find profession type [{profession}]")

    else:  # Neutral position
        if profession == "Professional":
            advice.append(
                "Walk the razor’s edge between the new and the old, a path fraught with peril. Master the balance of innovation and tradition to achieve unparalleled greatness.")
        elif profession == "Unemployed":
            advice.append(
                "Strive to balance the promise of change with the comfort of tradition. Embrace the duality of progress and preservation, forging a path that honors both.")
        elif profession == "Manual":
            advice.append(
                "Let innovation and tradition guide your hands in equal measure. Merge the best of both worlds to create something truly enduring and unique.")
        elif profession == "Business owner":
            advice.append(
                "Grow your enterprise with a blend of ancient wisdom and modern innovation. Build a legacy that stands the test of time, fueled by both the past and the future.")
        elif profession == "Public services":
            advice.append(
                "Serve both the old guard and the new order with a steady hand. Bridge the divide between tradition and change, ensuring the strength of your community.")
        elif profession == "Creative":
            advice.append(
                "Weave your art from the threads of both tradition and inspiration. Create works that resonate with the depth of history while capturing the spirit of the now.")
        elif profession == "Student":
            advice.append(
                "Study the lessons of both the past and the future. Become the scholar who sees the continuity in time, where the future is shaped by the wisdom of the past.")
        else:
            print(f"Could not find profession type [{profession}]")

    return advice


def generate_unhinged_relation_advice(relationship_status: str, collectivist_individualist: str,
                                      agnostic_spiritual: str, progressive_conservative: str):
    advice = []

    # Collectivist -- Individualist advice
    if collectivist_individualist == "collectivist":
        if relationship_status == "Married":
            advice.append(
                "Bind your souls so tightly that no force on earth, nor in the shadows beyond, can ever tear them apart. You shall be two as one, entwined in a bond so unbreakable that all shall tremble before the burning light of your love.")
        elif relationship_status == "Widowed":
            advice.append(
                "Embrace the sorrow shared by others, for in the depths of collective grief, you will uncover a power that transcends the mortal coil. Let the weight of their loss bury your own pain, merging your anguish with theirs until it becomes something more—something that binds you to the very essence of human existence. Bound, you shall be free.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Entwine your lives so completely that neither of you can remember a time before the other. Merge your dreams and fears into a singular existence, for only in absolute unity can you face whatever challenges come your way. Together, as one, you will find a strength that transcends the boundaries of your individual selves.")
        elif relationship_status == "Single":
            advice.append(
                "Let others into your life, consume their essence, and allow them to consume yours in return. The bonds you forge through this exchange will become the lifelines you cling to when the darkness encroaches. In this shared consumption, you will find a strength that binds you to others, a connection that endures even as the shadows gather around you.")
        elif relationship_status == "Separated":
            advice.append(
                "Lean on those who surround you, allowing their collective strength to pull you from the depths of separation. Embrace the power of the many, even as you feel yourself dissolving into the shared will of the group. Remember, it was the rejection of this unity that led to your past mistakes. This time, let the collective carry you, for in surrendering to their strength, you may finally find the peace that eluded you before. ")
        elif relationship_status == "Divorced":
            advice.append(
                "Reconstruct your shattered identity from the fragments offered by others. As you gather each piece, understand that it binds you to the collective forever. The more you take, the more you become entwined with the group, until your new self is a beautiful mosaic of shared experiences, inseparable from the whole.")
        elif relationship_status == "Engaged":
            advice.append(
                "Forge your union in the fires of public gaze, where every vow and promise is tempered by the scrutiny of those who watch. Let the intensity of their gaze strengthen your bond, forging a connection that is both undeniable and unbreakable under the weight of collective eyes.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif collectivist_individualist == "individualist":
        if relationship_status == "Married":
            advice.append(
                "Preserve your essence within the marriage, guarding it jealously. In a world where souls merge and identities blur, your individuality is the last bastion of your existence. Hold tight to what makes you uniquely you, for it is the one thing that must not be surrendered, even as everything else becomes intertwined.")
        elif relationship_status == "Widowed":
            advice.append(
                "Stand alone in your grief, a solitary pillar against the encroaching night. The path you walk now is yours alone, etched with the shadows of those who came before you. In this desolate journey, find strength in your solitude, for it is in the darkness that your true resilience will be revealed.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Hold tight to your mind and heart, for in love, it is all too easy to lose yourself. Guard your thoughts as sacred, and let your will remain unbreakable, even as the night grows darker. In the depths of passion and affection, remember who you are, for your inner light must not be extinguished by the shadows of desire.")
        elif relationship_status == "Single":
            advice.append(
                "Walk the solitary road with pride. Let the echoes of your footsteps be your only companion. In the silence of your journey, you will find the power to shape your own path, unbound by the presence or expectations of others.")
        elif relationship_status == "Separated":
            advice.append(
                "Reclaim your identity from the remnants of what was, and let no one dictate who you must become. You are a fortress, standing strong even as the walls close in. In the face of pressure and expectation, fortify your essence and resist the forces that seek to reshape you. Your identity is your own, and it will stand unbroken even though it has been broken before.")
        elif relationship_status == "Divorced":
            advice.append(
                "Sever the ties that once bound you with a clean, merciless cut. Stand alone, free from the weight of another’s expectations or dreams. Embrace your solitude as liberation, unburdened and unyielding, forging a path that is entirely your own.")
        elif relationship_status == "Engaged":
            advice.append(
                "Even as you prepare to merge your life with another, hold fast to the core of who you are. Let your individuality be the unwavering foundation upon which your union is built. In the blending of two lives, ensure that your unique essence remains intact, a beacon of strength and identity within the shared journey.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Balance your lives on the edge of a knife, for equilibrium is the only way to survive the tempest that rages around you. In the midst of chaos, find your footing together, where every step is a careful dance between stability and disaster. It is on this razor's edge that your strength is tested, and your bond is forged in the crucible of shared resilience.")
        elif relationship_status == "Widowed":
            advice.append(
                "Carry the torch of memory through the dark corridors of your soul, lighting the way forward even as shadows dance at the edges of your vision.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Find the stillness within the storm, the eye of the hurricane where your love can thrive, even as chaos consumes the world outside.")
        elif relationship_status == "Single":
            advice.append(
                "Tread carefully, for each step you take echoes into eternity. In the quiet of your solitude, the universe listens, waiting for your next move.")
        elif relationship_status == "Separated":
            advice.append(
                "Seek the calm within the maelstrom, for in the center of your inner chaos lies the clarity to see the world as it truly is.")
        elif relationship_status == "Divorced":
            advice.append(
                "Rebuild your life with hands steady and heart resolute, for the structure you create now will stand against the storms yet to come.")
        elif relationship_status == "Engaged":
            advice.append(
                "Prepare for the convergence of your lives with the solemnity of a ritual. The fusion of two souls is a sacred act, one that reshapes the very fabric of reality.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    # Agnostic -- Spiritual advice
    if agnostic_spiritual == "agnostic":
        if relationship_status == "Married":
            advice.append(
                "Question the very foundation of your union, for truth is forged in the crucible of doubt. Let your love be tested by the flames of skepticism. One can only truly love what one fully understands")
        elif relationship_status == "Widowed":
            advice.append(
                "Seek the silence beyond the grave, for in that stillness lie the answers to the questions you dared not ask them before. In the quiet of the departed, truths long buried may surface, revealing what was once hidden in the shadows of the living. ")
        elif relationship_status == "In a relationship":
            advice.append(
                "Delve deep into the mind of your partner, unravel the mysteries that lie hidden. Together, you will explore the uncharted realms of the human soul.")
        elif relationship_status == "Single":
            advice.append(
                "Do not mistake your inability to control when love happens for the remnants of some mystical force. Love's unpredictable nature is not magic—it's a stark reminder of the chaotic reality of human emotions. In the darkness of uncertainty, cling to logic and reason, for they are your only anchors in a world where feelings can surge unbidden, pulling you into depths you never chose to explore.")
        elif relationship_status == "Separated":
            advice.append(
                "Analyze the fractures in your life with cold precision, dissecting each crack and fault without flinching. In the stark clarity of this examination, you may uncover the key to mending what is broken. Only by facing the truth with unwavering honesty can you begin to piece together the shattered remnants")
        elif relationship_status == "Divorced":
            advice.append(
                "Peer into the depths of your soul, unflinching and unafraid, for the darkest truths hold the most brutal liberation. In the aftermath of divorce, confront the shadows within, where painful realities lie waiting. It is only by embracing these harsh truths that you can strip away the remnants of your past, leaving behind the illusions that once bound you.")
        elif relationship_status == "Engaged":
            advice.append(
                "Let your engagement be a crucible where beliefs are tested and reforged. In this intense fire, your bond will either emerge unbreakable, strengthened by the trials you face together, or it will crumble into ash, revealing what could not withstand the heat. Embrace the process, for only through this trial by fire will the true nature of your commitment be revealed.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")
    # TODO: Left off here
    elif agnostic_spiritual == "spiritual":
        if relationship_status == "Married":
            advice.append(
                "Entwine your spirits in a bond that transcends flesh and blood. Together, you shall walk the paths of the unseen, guided by forces beyond mortal comprehension.")
        elif relationship_status == "Widowed":
            advice.append(
                "Seek communion with the departed, let their voices guide your steps. The veil between worlds is thin, and through it, wisdom flows like a river of shadows.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Let your souls dance together in the twilight, where the boundaries of reality blur and merge. There, you will find a connection that defies the mortal coil.")
        elif relationship_status == "Single":
            advice.append(
                "Embrace the solitude of your soul, for in the quiet, the spirits gather to whisper secrets that only the truly alone can hear.")
        elif relationship_status == "Separated":
            advice.append(
                "Turn to the ancient rituals, the ones forgotten by time, for they hold the power to heal a heart torn asunder.")
        elif relationship_status == "Divorced":
            advice.append(
                "Purge the remnants of your past with fire and incantation, let the spirits cleanse you, so you may rise anew, reborn in the ashes of what was.")
        elif relationship_status == "Engaged":
            advice.append(
                "Prepare your spirit for the union to come, for when two souls merge, they create a force that can reshape the very fabric of existence.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Straddle the line between belief and doubt, where the answers lie in the tension between what is known and what is feared.")
        elif relationship_status == "Widowed":
            advice.append(
                "Hold the memory of your loved one like a candle in the dark, for in the glow, you will find the strength to face the shadows.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Explore the realms of both reason and faith with your partner, for only in the union of the two can true understanding be found.")
        elif relationship_status == "Single":
            advice.append(
                "Let your mind wander through the labyrinth of what is and what could be, for in the spaces between thoughts, reality takes shape.")
        elif relationship_status == "Separated":
            advice.append(
                "Seek the wisdom of both the seen and the unseen, for in understanding both, you will find the clarity to rebuild what has been torn apart.")
        elif relationship_status == "Divorced":
            advice.append(
                "Balance the rational and the mystical as you reconstruct your life, for in the blending of the two, you will find a strength unyielding.")
        elif relationship_status == "Engaged":
            advice.append(
                "Prepare your union to be a melding of both mind and spirit, for only through the harmony of the two can the bond endure the trials to come.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    # Progressive -- Conservative advice
    if progressive_conservative == "progressive":
        if relationship_status == "Married":
            advice.append(
                "Tear down the walls that confine your union, rebuild it with the stones of revolution. Your marriage shall be the spark that ignites a new world.")
        elif relationship_status == "Widowed":
            advice.append(
                "Turn your back on the past, forge a path through the wilderness of the unknown. In the ashes of yesterday, you will find the seeds of tomorrow.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Embrace the chaos of change, let it mold and shape your bond into something new, something that defies the very nature of what once was.")
        elif relationship_status == "Single":
            advice.append(
                "Shatter the chains of tradition, walk a path untraveled and unseen. You are the architect of a future no one else can imagine.")
        elif relationship_status == "Separated":
            advice.append(
                "Rise from the ruins of your former life like a phoenix from the flames. Let the past be nothing but kindling for the fire of your rebirth.")
        elif relationship_status == "Divorced":
            advice.append(
                "Erase the remnants of what was, carve a new destiny from the bones of the old. In the death of the past lies the birth of the future.")
        elif relationship_status == "Engaged":
            advice.append(
                "Let your union be a beacon of change, a defiance against the forces that would hold you to the past. Together, you will forge a new path through the wilderness.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    elif progressive_conservative == "conservative":
        if relationship_status == "Married":
            advice.append(
                "Cling to the ancient ways, let tradition be the bedrock upon which your marriage is built. In the old ways, you will find strength that time cannot erode.")
        elif relationship_status == "Widowed":
            advice.append(
                "Wrap yourself in the comfort of the past, let the echoes of bygone days guide your steps. In the wisdom of the ancestors, you will find the solace you seek.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Root your bond in the soil of tradition, let the growth of your love be slow and steady, nourished by the wisdom of those who came before.")
        elif relationship_status == "Single":
            advice.append(
                "Walk the well-trodden path of those who came before you, for in their footsteps, you will find the safety and stability that the future cannot promise.")
        elif relationship_status == "Separated":
            advice.append(
                "Return to the foundations of your life, let the solidity of tradition support you as you rebuild. The old ways have withstood the test of time for a reason.")
        elif relationship_status == "Divorced":
            advice.append(
                "Rebuild your life upon the sturdy bones of the past, for in the old ways, you will find the structure needed to face the uncertainty of what is to come.")
        elif relationship_status == "Engaged":
            advice.append(
                "Prepare for your union with the reverence and solemnity of ages past. In the traditions of your ancestors, you will find the strength to forge a future together.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    else:  # Neutral position
        if relationship_status == "Married":
            advice.append(
                "Walk the tightrope between tradition and progress, for in the balance lies the strength to face the unknown together.")
        elif relationship_status == "Widowed":
            advice.append(
                "Stand at the crossroads of past and future, for in choosing your path, you will find the power to shape what is yet to come.")
        elif relationship_status == "In a relationship":
            advice.append(
                "Blend the stability of the past with the promise of the future, for in the fusion of the two, your bond will grow unbreakable.")
        elif relationship_status == "Single":
            advice.append(
                "Let your steps be guided by both the wisdom of ages and the daring of youth, for in the harmony of the two, your path will lead you to places unseen.")
        elif relationship_status == "Separated":
            advice.append(
                "Rebuild your life by drawing on both the lessons of the past and the possibilities of the future. In this union, you will find the strength to rise again.")
        elif relationship_status == "Divorced":
            advice.append(
                "Anchor yourself in the traditions that have stood the test of time, while reaching toward the unknown. This balance will give you the stability you seek.")
        elif relationship_status == "Engaged":
            advice.append(
                "Prepare your future together by honoring the past and embracing the new, for in the confluence of these forces, your union will be forged unbreakable.")
        else:
            print(f"Could not find relationship type [{relationship_status}]")

    return advice