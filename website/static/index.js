function deleteNote(noteId) {
    fetch("/delete-report", {
      method: "POST",
      body: JSON.stringify({ reportId: reportId }),
    }).then((_res) => {
      window.location.href = "/admin_page";
    });
  }