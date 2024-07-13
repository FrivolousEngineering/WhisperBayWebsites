// First off, I am so sorry. Javascript doesn't support seeds, so we have to do a whole bunch of weird shit to get this to work.
// The reason we want this is because we want randomly colored buttons. This is how we get them. 
function cyrb128(str) {
  let h1 = 1779033703, h2 = 3144134277,
      h3 = 1013904242, h4 = 2773480762;
  for (let i = 0, k; i < str.length; i++) {
      k = str.charCodeAt(i);
      h1 = h2 ^ Math.imul(h1 ^ k, 597399067);
      h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
      h3 = h4 ^ Math.imul(h3 ^ k, 951274213);
      h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
  }
  h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
  h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
  h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
  h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
  h1 ^= (h2 ^ h3 ^ h4), h2 ^= h1, h3 ^= h1, h4 ^= h1;
  return [h1>>>0, h2>>>0, h3>>>0, h4>>>0];
}
function sfc32(a, b, c, d) {
    return function() {
      a |= 0; b |= 0; c |= 0; d |= 0;
      let t = (a + b | 0) + d | 0;
      d = d + 1 | 0;
      a = b ^ b >>> 9;
      b = c + (c << 3) | 0;
      c = (c << 21 | c >>> 11);
      c = c + t | 0;
      return (t >>> 0) / 4294967296;
    }
}
function getRandomColor(modifier = 0) {
    const currentTime = new Date();
    const minutes = currentTime.getMinutes();
    const timeSegment = Math.floor(minutes / 5) + modifier;
    const timeSegment2 = currentTime.getHours() * 12 + timeSegment; // Unique seed for each 5-minute segment
    var seed = cyrb128("someseed" + timeSegment2.toString());
    var rand = sfc32(seed[0], seed[1], seed[2], seed[3]);

    const r = Math.floor(rand() * 256);
    const g = Math.floor(rand() * 256);
    const b = Math.floor(rand() * 256);
    console.log(timeSegment);
    console.log(`rgb(${r},${g},${b})`);
    return `rgb(${r},${g},${b})`;
}

function applyRandomColor() {
    const randomColor = getRandomColor();
    const randomColor2 = getRandomColor(100);
    const randomColor3 = getRandomColor(200);
    const menuItems = document.querySelectorAll('.menu-item');
    const linkItems = document.querySelectorAll('.link-item');
    const header = document.querySelectorAll("#header");
    menuItems.forEach(item => item.style.backgroundColor = randomColor);
    linkItems.forEach(item => item.style.backgroundColor = randomColor2);
    header.forEach(item => item.style.backgroundColor = randomColor3);
}

document.addEventListener('DOMContentLoaded', applyRandomColor);

document.getElementById('links').addEventListener('scroll', function() {
    var links = document.getElementById('links');
    var seeMore = document.getElementById('seeMore');
    if (links.scrollTop + links.clientHeight >= links.scrollHeight) {
        seeMore.classList.add('disabled');
    } else {
        seeMore.classList.remove('disabled');
    }
});
