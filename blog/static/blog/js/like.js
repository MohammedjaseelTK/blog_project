document.addEventListener("DOMContentLoaded", function () {
  console.log("Like.js loaded ✅");  // test if file is connected

  const likeButtons = document.querySelectorAll(".like-btn");
  likeButtons.forEach(btn => {
    btn.addEventListener("click", function () {
      console.log("Heart clicked ❤️"); // test click
      this.classList.toggle("fa-solid");
      this.classList.toggle("fa-regular");
      this.classList.toggle("text-red-500");
    });
  });
});
