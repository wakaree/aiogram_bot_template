import { Message } from "grammy/types";

export interface ConfigCommandHandlers {
  path: string;
  handler: Function;
}
export interface TextMessageConversationHandler {
  title: string;
  msg: Message;
}

export interface CallbackQueryMessageConversationHandler<T> {
  messageId: number;
  choice: T;
}
