import { SessionFlavor, Context } from "grammy";
import { BotSession } from "./session";

export type BotContext = Context & SessionFlavor<BotSession>;
