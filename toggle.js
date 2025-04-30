 /*toggle leadboards*/
 function toggleLeaderboard() {
    const leaderboard = document.querySelector('.leaderboard');
    if (leaderboard.style.display === 'none') {
      leaderboard.style.display = 'block'; // Show the leaderboard
    } else {
      leaderboard.style.display = 'none'; // Hide the leaderboard
    }
  }
  /* Toggle Publication Form */
function togglePublication() {
    const publicationForm = document.getElementById('publicationForm');
    if (publicationForm.style.display === 'none') {
      publicationForm.style.display = 'block'; // Show the form
    } else {
      publicationForm.style.display = 'none'; // Hide the form
    }
  }
  function toggleAskForm() {
    const askForm = document.getElementById('askDoctorForm');
    if (askForm.style.display === 'none') {
      askForm.style.display = 'block'; // Show the form
    } else {
      askForm.style.display = 'none'; // Hide the form
    }
  }
  function toggleArticle(button) {
    const articleContent = button.previousElementSibling; // Get the hidden content
    if (articleContent.style.display === "none") {
      articleContent.style.display = "block"; // Show the content
      button.textContent = "اقرأ أقل"; // Change button text
    } else {
      articleContent.style.display = "none"; // Hide the content
      button.textContent = "اقرأ المزيد"; // Change button text
    }
  }