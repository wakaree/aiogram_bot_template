import { Conversation } from "@grammyjs/conversations";
import { Context } from "vm";

const createTask = async (conversation: Conversation, ctx: Context) => {
  await ctx.reply("Hi there! What is your name?");
  const { message } = await conversation.waitFor("message:text");
  await ctx.reply(`Welcome to the chat, ${message.text}!`);
};
