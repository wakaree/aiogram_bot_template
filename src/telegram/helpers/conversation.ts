import { MyConversation } from "../type/conversation";
import {
  CallbackQueryMessageConversationHandler,
  TextMessageConversationHandler,
} from "../type/handler";

export const handlerMessage = async (
  handlerSend: () => Promise<void>,
  handlerGet: () => Promise<TextMessageConversationHandler>,
): Promise<TextMessageConversationHandler> => {
  await handlerSend();
  return await handlerGet();
};
export const handlerGetTextMessage = async (
  conversation: MyConversation,
): Promise<TextMessageConversationHandler> => {
  const msg = await conversation.waitFor("message:text");
  const title = msg.message.text;
  return { title, msg: msg.message };
};
export const handlerGetCallbackQueryMessage = async <T extends string>(
  conversation: MyConversation,
): Promise<CallbackQueryMessageConversationHandler<T>> => {
  const action = await conversation.waitFor("callback_query:data");
  const choice = action.callbackQuery.data as T;
  const messageId = action.callbackQuery.message?.message_id ?? 0;
  await action.answerCallbackQuery();

  return { messageId, choice };
};
