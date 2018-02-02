chrome.webRequest.onBeforeRequest.addListener(
  callback = function(details) {
    if(details.method != 'POST') {
      return;
    }
    if(details['requestBody'].hasOwnProperty('formData') != true){
      return;
    }
    if(details['requestBody']['formData'].hasOwnProperty('content') != true){
      return;
    }
      //console.log('POST Intercepted ' + decodeURIComponent(JSON.stringify(details['requestBody']['formData']['content'])));
      //var txt = decodeURIComponent(JSON.stringify(details['requestBody']['formData']['content']));
      var txt = decodeURIComponent(JSON.stringify(details['requestBody']));
      //var txt2 = unescape(decodeURIComponent(JSON.stringify(details['requestBody'])));
      //console.log(txt2);
      phone = txt.match(/\d{3}-\d{3,4}-\d{4}/g);
      email = txt.match(/[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}/g);
      if((phone == null) & (email == null)) {
        return;
      }
      if(confirm('Personally identifiable information may be exposed. Would you like to continue?\n----[ Phone number ]----\n' + phone + '\n----[ email address ]----\n' + email) == false) {
        return {cancel: true};
      }
      txt = 'It\'s been 30 days since your personally identifiable information was exposed. Your personally identifiable information is still being exposed.\n[Joonggonara Title] ' + decodeURIComponent(JSON.stringify(details['requestBody']['formData']['subject']));
      chrome.alarms.create(txt, {'when': Date.now() + 3000})
  },
  filter = {
    urls: ["*://cafe.naver.com/TempsavePost.nhn"]
  },
  opt_extraInfoSpec = [
    "requestBody",
    "blocking"
  ]
);

chrome.alarms.onAlarm.addListener(
  callback = function(alarm) {
    chrome.notifications.create({'type': 'basic', 
                                 'iconUrl': 'TIMG012.png',
                                 'title': 'Remind PII Notification',
                                 'message': alarm.name})
  }
);