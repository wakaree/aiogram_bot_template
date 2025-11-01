import { SessionFlavor, Context } from "grammy";
import { BotSession } from "./session";
import { User } from "../../models/user.model";
import { I18nFlavor } from "@grammyjs/i18n";
import { ConversationFlavor } from "@grammyjs/conversations";

export type BotContext = Context & SessionFlavor<BotSession> & I18nFlavor;
export type UserContext = BotContext &
  ConversationFlavor<BotContext> & {
    user: User;
  };
