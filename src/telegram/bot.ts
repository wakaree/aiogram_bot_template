import { Bot, session } from "grammy";
import { botConfig } from "../config/bot";
import { BotContext, UserContext } from "./type/context";
import { router } from "./handlers/router";
import { BotSession } from "./type/session";
import { I18n } from "@grammyjs/i18n";
import {
  type ConversationFlavor,
  createConversation,
  conversations,
} from "@grammyjs/conversations";
import { createTaskConversation } from "./conversations/create-task";
import { userMiddleware } from "./middlewars/user";
export const bot = new Bot<UserContext>(botConfig.bot_token);
export const i18n = new I18n<UserContext>({
  defaultLocale: "en",
  directory: `${process.cwd()}/assets/locales`,
  fluentBundleOptions: { useIsolating: false },
  useSession: true,
});

export const intiBot = () => {
  bot.use(
    session({
      initial: () => {
        return {};
      },
    }),
  );
  bot.use(i18n);
  bot.use(userMiddleware);
  bot.use(conversations());
  bot.use(createConversation(createTaskConversation));
  bot.use(router);
  bot
    .start({
      onStart: () => console.log("Bot connected"),
    })
    .catch((err) => console.error("Bot failed to start:", err));
};
