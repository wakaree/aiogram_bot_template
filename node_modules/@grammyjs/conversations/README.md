# <h1 align="center">grammY conversations</h1>

---

The grammY conversations plugin lets you create powerful conversational interfaces with ease.

> This is version 2 of the plugin.
> Version 2 is a complete rewrite from scratch.
> If you are still using version 1.x, check out [the migration guide](https://grammy.dev/plugins/conversations#migrating-from-1-x-to-2-x).
> (The old docs are no longer be updated but they can still be found [here](https://6797de6b803511577fcb38ad--grammy.netlify.app/plugins/conversations).)

You should check out [the official documentation](https://grammy.dev/plugins/conversations) of the plugin, but here is a quickstart for you to get up and running.

## Quickstart

Run `npm i @grammyjs/conversations` and paste the following code:

```ts
import { Bot, type Context } from "grammy";
import {
    type Conversation,
    type ConversationFlavor,
    conversations,
    createConversation,
} from "@grammyjs/conversations";

type MyContext = ConversationFlavor<Context>;
type MyConversationContext = Context;

type MyConversation = Conversation<MyContext, MyConversationContext>;

const bot = new Bot<MyContext>("");

/** Defines the conversation */
async function greeting(
    conversation: MyConversation,
    ctx: MyConversationContext,
) {
    await ctx.reply("Hi there! What is your name?");
    const { message } = await conversation.wait();
    await ctx.reply(`Welcome to the chat, ${message.text}!`);
}

bot.use(conversations());
bot.use(createConversation(greeting));

bot.command("enter", async (ctx) => {
    await ctx.reply("Entering conversation!");
    // enter the function "greeting" you declared
    await ctx.conversation.enter("greeting");
});

bot.command("start", (ctx) => ctx.reply("Hi! Send /enter"));
bot.use((ctx) => ctx.reply("What a nice update."));

bot.start();
```

Nifty!
