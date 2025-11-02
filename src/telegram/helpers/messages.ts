import { InlineKeyboard } from "grammy";
import { bot } from "../bot";
import { BotContext } from "../type/context";
import { Message } from "grammy/types";

export const factorySend = async (
  handlerSend: (
    message: string,
    keyboard: InlineKeyboard,
  ) => Promise<Message.TextMessage>,
  message: string,
  keyboard: string[][] = [],
): Promise<Message.TextMessage> => {
  const buttonRow = keyboard.map(([label, data]) =>
    InlineKeyboard.text(label, data),
  );
  const keyboards = InlineKeyboard.from([buttonRow]);
  return await handlerSend(message, keyboards);
};
export const sendMessage = async (
  id: number,
  message: string,
  keyboard: string[][] = [],
) => {
  const handler = async (
    message: string,
    keyboard: InlineKeyboard,
  ): Promise<Message.TextMessage> => {
    return await bot.api.sendMessage(id, message, {
      reply_markup: keyboard,
    });
  };
  await factorySend(handler, message, keyboard);
};
export const editMessage = async (
  chatId: number,
  messageId: number,
  message: string,
  keyboard: string[][] = [],
) => {
  const handler = async (
    message: string,
    keyboard: InlineKeyboard,
  ): Promise<Message.TextMessage> => {
    try {
      return (await bot.api.editMessageText(chatId, messageId, message, {
        reply_markup: keyboard,
      })) as Message.TextMessage;
    } catch (error: any) {
      if (
        error.error_code === 400 &&
        error.description?.includes("message is not modified")
      ) {
        return { message_id: messageId } as Message.TextMessage;
      }
      throw error;
    }
  };
  await factorySend(handler, message, keyboard);
};
export const sendReply = async (
  ctx: BotContext,
  message: string,
  keyboard: string[][] = [],
): Promise<Message.TextMessage> => {
  const handler = async (
    message: string,
    keyboard: InlineKeyboard,
  ): Promise<Message.TextMessage> => {
    return await ctx.reply(message, {
      reply_markup: keyboard,
    });
  };
  return await factorySend(handler, message, keyboard);
};
