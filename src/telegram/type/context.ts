import { SessionFlavor, Context } from "grammy";
import { BotSession } from "./session";
import { User } from "../../models/user.model";

export type BotContext = Context & SessionFlavor<BotSession>;
export interface UserContext extends BotContext {
  user: User;
}
