import { CreateUserChat } from "../models/user-chat.model";
import { createUserChatRepo } from "../repo/user-chat.repo";

export const createUserChat = async (chatId: number, userId: number) => {
  const userChatData: CreateUserChat = {
    chatId: chatId,
    userId: userId,
  };
  const userChat = await createUserChatRepo(userChatData);
  return userChat;
};
export const findOneByIdUserChat = async (chatId: string) => { };
