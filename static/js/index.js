document.addEventListener("DOMContentLoaded", function () {
  let toasts = document.querySelectorAll(".toast");
  toasts.forEach((toastEl) => {
    let toast = new bootstrap.Toast(toastEl);
    toast.show();
  });
});