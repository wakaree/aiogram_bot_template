import { UserContext } from "../type/context";

export const homeKeyboard = async (ctx: UserContext): Promise<string[][]> => {
  return [
    [ctx.t("startButtonChooseAction"), "startCreateTask"],
    [ctx.t("watchButtonChooseAction"), "watchTask"],
  ];
};
