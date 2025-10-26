import { InlineKeyboard } from "grammy";
import { bot } from "../bot";

export const sendMessage = async (
  id: string,
  message: string,
  keyboard: string[][] = [],
) => {
  const buttonRow = keyboard.map(([label, data]) =>
    InlineKeyboard.text(label, data),
  );
  const keyboards = InlineKeyboard.from([buttonRow]);
  await bot.api.sendMessage(id, message, {
    reply_markup: keyboards,
  });
};
