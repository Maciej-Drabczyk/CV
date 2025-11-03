var CurrentlyShownEmail = 0

document.addEventListener('DOMContentLoaded', function() {


  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Adding events to email buttons
  document.querySelector('#reply_button').addEventListener('click', () => reply_email(CurrentlyShownEmail))
  document.querySelector('#archive_button').addEventListener('click', () => archive_email(CurrentlyShownEmail, true))
  document.querySelector('#unarchive_button').addEventListener('click', () => archive_email(CurrentlyShownEmail, false))

  // Composing email function on submit of form
  document.querySelector('#compose-form').onsubmit = function(e) {
    e.preventDefault()
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        load_mailbox('sent')
    });
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none'
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none'
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load emails of correct mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
          if(email['read']) {
            document.querySelector('#emails-view').insertAdjacentHTML('beforeend',
             `<div class="container email_preview bg-light" data-id="${email['id']}">
                <b>${email['sender']}</b>
                <p>${email['subject']}</p>
                <small>${email['timestamp']}</small>
              </div>`
            );
          } else {
            document.querySelector('#emails-view').insertAdjacentHTML('beforeend',
             `<div class="container email_preview" data-id="${email['id']}">
                <b>${email['sender']}</b>
                <p>${email['subject']}</p>
                <small>${email['timestamp']}</small>
             </div>`
            );
          }
    });

    document.querySelectorAll('.email_preview').forEach(email => {
      email.addEventListener('click', () => read_email(email, mailbox))
    })
  })
}

function read_email(email, source) {
  // Marking email as read
  const id = email.dataset.id
  if(source != "sent") {
    fetch(`emails/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        read: true
      })
    })
  }
  show_email(email, source)
}

function show_email(email, source) {
  // Loading email's content
  const id = email.dataset.id

  fetch(`emails/${id}`)
  .then(respones => respones.json())
  .then(email => {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block'
    document.querySelector('#compose-view').style.display = 'none';
    CurrentlyShownEmail = id
    document.querySelector('#email_from').innerHTML = `<b>From: </b>${email['sender']}`
    document.querySelector('#email_to').innerHTML = `<b>To: </b>${email['recipients']}`
    document.querySelector('#email_subject').innerHTML = `<b>Subject: </b>${email['subject']}`
    document.querySelector('#email_timestamp').innerHTML = `<b>Timestamp: </b>${email['timestamp']}`
    document.querySelector('#email_body').innerHTML = `${email['body']}`

    // Displaying proper buttons
    if(source != 'sent') {
      document.querySelector('#reply_button').style.display = 'block'
    } else {
      document.querySelector('#reply_button').style.display = 'none'
    }

    if(source != 'sent' && !email['archived']) {
      document.querySelector('#archive_button').style.display = 'block'
    } else {
      document.querySelector('#archive_button').style.display = 'none'
    }

    if(source == "archive" && email['archived']) {
      document.querySelector('#unarchive_button').style.display = 'block'
    } else {
      document.querySelector('#unarchive_button').style.display = 'none'
    }
  })
}

function reply_email(id) {
  // Replying to email and filling certain form parts
  console.log(id)
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email)
    document.querySelector('#compose-recipients').value = email['sender'];
    document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
    document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote:\n"${email['body']}"\n`;

    document.querySelector('#emails-view').style.display = 'none'
    document.querySelector('#email-view').style.display = 'none'
    document.querySelector('#compose-view').style.display = 'block'
  })

}

function archive_email(id, toggle) {
  // Place email to archive
  fetch(`emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: toggle
    })
  })
  reload_archive(toggle)
}

function reload_archive(archived) {
  // Change archive buttons based on if email is archived
  if (archived) {
      document.querySelector('#archive_button').style.display = 'none'
      document.querySelector('#unarchive_button').style.display = 'block'
  } else {
      document.querySelector('#archive_button').style.display = 'block'
      document.querySelector('#unarchive_button').style.display = 'none'
  }
}