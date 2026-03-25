import type { Item } from '@/types';

const wait = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

export async function createItemService(item: Item): Promise<Item> {
  await wait();
  return structuredClone(item);
}

export async function updateItemService(item: Item): Promise<Item> {
  await wait();
  return structuredClone(item);
}

export async function deleteItemService(itemId: number): Promise<number> {
  await wait();
  return itemId;
}
