import "bootstrap";
import "./fontawesome/all.min.js";

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

const checkBoxes = document.querySelectorAll(`input[type="checkbox"]`);
checkBoxes.forEach((checkbox) => {
  checkbox.addEventListener("click", (e) => {
    const lead_id = e.currentTarget.id.match(/\d/)[0];
    const checkbox_value = e.currentTarget.checked;
    fetch(`${window.location.origin}/api/leads/${lead_id}`, {
      method: "PATCH",
      body: JSON.stringify({
        isAnswered: checkbox_value,
      }),
      headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
      }
    })
      .then((res) => console.log(res))
      .catch((err) => console.error(err));
  });
});
