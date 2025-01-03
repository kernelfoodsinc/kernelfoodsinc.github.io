const gForm         = document.getElementById("gform");
const gFormLoading  = document.getElementById("gFormLoading");
const gFormSuccess  = document.getElementById("gformSuccess");
const gFormRecall   = document.getElementById("gFormRecall");
let submitted       = localStorage.getItem("eatkernel.com__gform__01.2025")

gForm.addEventListener("submit", () => {

  localStorage.setItem("eatkernel.com__gform__01.2025", true)
  gFormLoading.style.display = "block";
  gForm.style.display = "none";

  setTimeout(function () {
    gFormLoading.style.display = "none";
    gFormSuccess.style.display = "block";
  }, 1000);

});

gFormRecall.addEventListener("load", () => {
  if (submitted) {
    // 
  
  }
});

window.addEventListener("load", () => {
    if(submitted){
        gForm.style.display = "none"
        
        gFormLoading.style.display = "none";
        gFormSuccess.style.display = "block";
    }
})
