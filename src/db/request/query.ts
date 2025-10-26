import { snakeToCamel } from "../../utils/snakeToCamel";
import { pool } from "../connect";

export const query = async <T extends Record<string, any>>(
  text: string,
  params?: any[],
): Promise<T[]> => {
  const result = await pool.query(text, params);

  return result.rows.map((row) => snakeToCamel<T>(row));
};
