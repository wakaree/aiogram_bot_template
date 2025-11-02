import { Day } from "../../enums/day.enum";
import { CreateScheduledTime } from "../../models/scheduled-time.model";
import { i18n } from "../bot";
import { DayKeyboardEnum } from "../enum/day-keyboard.enum";
import {
  handlerGetCallbackQueryMessage,
  handlerGetTextMessage,
} from "../helpers/conversation";
import { editMessage, sendMessage, sendReply } from "../helpers/messages";
import {
  dayAddKeyboard,
  dayChooseKeyboard,
} from "../key-board/create-task-keyboard";
import { ScheduledTimeConversation } from "../model/sheduled-time-conversation";
import { BotContext } from "../type/context";
import { MyConversation } from "../type/conversation";
import { waitForValidMessage } from "../utils/wait-for-valid-message";

export const scheduledTimesConversation = async (
  conversation: MyConversation,
  ctx: BotContext,
  idMessage: number,
): Promise<CreateScheduledTime[]> => {
  const locale = await conversation.external(
    () => ctx.session?.__language_code || "en",
  );
  const scheduledTimes: CreateScheduledTime[] = [];
  let dayButton = await dayChooseKeyboard((name: string) =>
    i18n.t(locale, name),
  );
  while (true) {
    const time = await scheduledTimeConversation(
      conversation,
      ctx,
      idMessage,
      dayButton,
    );
    if (time == "next") {
      break;
    }
    const day = scheduledTimes.find((elem) => elem.day == time.day);
    const dayIndex = scheduledTimes.findIndex((elem) => elem.day == time.day);
    if (day) {
      day.timeSlots = [...day.timeSlots, time.timeSlots];
      scheduledTimes[dayIndex] = day;
    } else {
      scheduledTimes.push({
        day: time.day,
        timeSlots: [time.timeSlots],
      });
    }
    const newDay = scheduledTimes.find((elem) => elem.day == time.day);
    if (!newDay) throw Error();
    const messageScheduledTimes = await sendReply(
      ctx,
      i18n.t(locale, "scheduledTimes", {
        day: newDay?.day,
        times: newDay?.timeSlots.join(", "),
      }),
    );
    idMessage = messageScheduledTimes.message_id ?? idMessage;
    dayButton = await dayAddKeyboard((name: string) => i18n.t(locale, name));
  }
  return scheduledTimes;
};
export const scheduledTimeConversation = async (
  conversation: MyConversation,
  ctx: BotContext,
  idMessage: number,
  button: string[][],
): Promise<ScheduledTimeConversation | "next"> => {
  if (!ctx?.chat?.id) throw Error;
  const choiceChooseDay = await chooseDayConversation(
    conversation,
    ctx,
    idMessage,
    button,
  );
  if (choiceChooseDay === DayKeyboardEnum.createTaskTime) {
    return "next";
  }
  const selectedDay: Day = Object.entries(DayKeyboardEnum).find(
    ([, v]) => v === choiceChooseDay,
  )?.[0] as Day;
  const time = await chooseTimeConversation(
    conversation,
    ctx,
    idMessage,
    selectedDay,
  );
  return {
    day: selectedDay,
    timeSlots: time,
  };
};
export const chooseTimeConversation = async (
  conversation: MyConversation,
  ctx: BotContext,
  idMessage: number,
  selectedDay: Day,
): Promise<string> => {
  const locale = await conversation.external(
    () => ctx.session?.__language_code || "en",
  );
  const handlerChooseTime = async () => {
    if (!ctx?.chat?.id) throw Error;
    await editMessage(
      ctx.chat.id,
      idMessage,
      i18n.t(locale, "chooseTime", { day: selectedDay }),
    );
  };
  const handlerInvalidSendMessage = async () => {
    if (!ctx?.chat?.id) throw Error;
    await sendReply(ctx, i18n.t(locale, "chooseTime", { day: selectedDay }));
  };
  const { title: time } = await waitForValidMessage(
    new RegExp("^([01]\\d|2[0-3]):[0-5]\\d$"),
    handlerChooseTime,
    handlerInvalidSendMessage,
    () => handlerGetTextMessage(conversation),
  );
  return time;
};
export const chooseDayConversation = async (
  conversation: MyConversation,
  ctx: BotContext,
  idMessage: number,
  button: string[][],
): Promise<DayKeyboardEnum> => {
  if (!ctx?.chat?.id) throw Error;
  const locale = await conversation.external(
    () => ctx.session?.__language_code || "en",
  );

  const text = i18n.t(locale, "chooseDay") + " ";
  await editMessage(ctx.chat.id, idMessage, text, button);
  const { choice: choiceChooseDay } =
    await handlerGetCallbackQueryMessage<DayKeyboardEnum>(conversation);

  return choiceChooseDay;
};
