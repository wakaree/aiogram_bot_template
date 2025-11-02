import { NextFunction } from "grammy";
import { getOrCreateUserAndChat } from "../../services/user.service";
import { ValidationError } from "../../errors/validation-errors";
import { UserContext } from "../type/context";

export const userMiddleware = async (
  ctx: UserContext,
  next: NextFunction,
): Promise<void> => {
  const telegramUser = ctx.from;
  if (!telegramUser) {
    throw new ValidationError("Telegram user not found in the context");
  }

  const chatId = ctx.chat?.id;
  if (!chatId) {
    throw new ValidationError("Chat ID is missing in the context");
  }

  const user = await getOrCreateUserAndChat(telegramUser, chatId);
  ctx.user = user;

  await next();
};
