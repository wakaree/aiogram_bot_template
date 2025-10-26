import { Bot, session } from "grammy";
import { botConfig } from "../config/bot";
import { BotContext } from "./type/context";
import { router } from "./handlers/router";
import { BotSession } from "./type/session";

export const bot = new Bot<BotContext>(botConfig.bot_token);

export const intiBot = () => {
  bot.use(session<BotSession, BotContext>());
  bot.use(router);
  bot
    .start({
      onStart: () => console.log("Bot connected"),
    })
    .catch((err) => console.error("Bot failed to start:", err));
};
