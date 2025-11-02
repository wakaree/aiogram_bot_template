import { TextMessageConversationHandler } from "../type/handler";

export const waitForValidMessage = async (
  reg: RegExp,
  handlerSendMessage: () => Promise<void>,
  handlerInvalidSendMessage: () => Promise<void>,
  handlerGetMessage: () => Promise<TextMessageConversationHandler>,
): Promise<TextMessageConversationHandler> => {
  await handlerSendMessage();

  let msg = await handlerGetMessage();
  let title = msg.title;

  while (!reg.test(title)) {
    await handlerInvalidSendMessage();
    msg = await handlerGetMessage();
    title = msg.title;
  }

  return msg;
};
