import { pool } from "../connect";

export const query = async <T>(text: string, params?: any[]): Promise<T[]> => {
  const result = await pool.query(text, params);
  return result.rows as T[];
};
