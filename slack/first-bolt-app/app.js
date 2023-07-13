const { App, LogLevel } = require('@slack/bolt');

// ボットトークンと Signing Secret を使ってアプリを初期化します
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
  port: process.env.PORT || 3000,
  logLevel: LogLevel.DEBUG,
});


workfolws = [
  hello_workflow(app),
  mention_workflow(app),
]

function hello_workflow(app) {
  return async () => {
    app.message('hello', async ({ message, say }) => {
      await say({
        blocks: [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "hello"
            },
            "accessory": {
              "type": "button",
              "text": {
                "type": "plain_text",
                "text": "Click Me"
              },
              "action_id": "button_click"
            }
          }
        ],
        text: "hello"
      });
    });

    app.action('button_click', async ({ body, ack, say }) => {
      await ack();
      await say(`<@${body.user.id}> clicked the button`);
    });
  }
}

function mention_workflow(app){
  return async () => {
    app.event('app_mention', async ({ event, say }) => {
      await say(`Hey there <@${event.user}>!`);
    });
  }
}


for (const workflow of workfolws) {
  workflow.call();
}


(async () => {
  // アプリを起動します
  await app.start();

  console.log('⚡️ Bolt app is running!');
})();


