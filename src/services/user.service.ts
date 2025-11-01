import type { User as TelegramUser } from "@grammyjs/types";
import { createUserRepo, findOneByIdRepo } from "../repo/user.repo";
import { CreateUser, User } from "../models/user.model";
import { createUserChat } from "./user-chat.service";

export const getOrCreateUserAndChat = async (
  data: TelegramUser,
  chatId: number,
): Promise<User> => {
  let user: User | undefined = await findOneByIdRepo(data.id);
  if (!user) {
    user = await createUser(data);
  }
  if (!user.userChats) {
    user.userChats = [];
  }
  const userChat = user.userChats.find((elem) => elem.chatId === chatId);

  if (!userChat) {
    const newUserChat = await createUserChat(chatId, user.telegramId);
    user.userChats.push(newUserChat);
  }
  return user;
};
export const createUser = async (data: TelegramUser): Promise<User> => {
  const body: CreateUser = {
    telegramId: data.id,
    username: data?.username,
    firstName: data?.first_name,
    lastName: data?.last_name,
  };
  const user = await createUserRepo(body);
  return user;
};
