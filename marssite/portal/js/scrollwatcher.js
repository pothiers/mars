
export default function(){
  if (document.querySelector("[rel=form-submit]") === null) {
    return;
  }

  const doc = document.documentElement;
  const top = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
  const element = document.querySelector("[rel=form-submit]");
  const elementTop = element.offsetTop;

  // check offset
  if (top > elementTop) {
    element.classList.add("scroll");
  } else {
    element.classList.remove("scroll");
  }
};
