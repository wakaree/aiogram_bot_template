import { Conversation, ConversationFlavor } from "@grammyjs/conversations";
import { UserContext } from "./context";

export type MyConversation = Conversation<
  ConversationFlavor<UserContext>,
  UserContext
>;
