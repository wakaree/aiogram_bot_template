import { Conversation, ConversationFlavor } from "@grammyjs/conversations";
import { BotContext } from "./context";

export type MyConversation = Conversation<
  ConversationFlavor<BotContext>,
  BotContext
>;
