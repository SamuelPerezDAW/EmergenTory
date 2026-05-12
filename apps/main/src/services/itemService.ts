import type { Item } from '@/types';
import axios from 'axios';

const wait = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

export async function createItemService(item: Item, matricula: string): Promise<Item | undefined> {
  await wait();

  const response = await axios.post(`http://127.0.0.1:8000/api/checklists/checkitems/add/`, {
    'nombre': item.nombre,
    'activo': item.activo,
    'checklist': matricula,
  },{
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`
    }
  });

  const status = response.status;
  const data = response.data;
  
  if (status == 200){  
    try {
      if (typeof data === 'object'){
        return structuredClone(item);
      }
    } catch(error) {
      console.log("ERROR: ", error);
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
  }
}

export async function updateItemService(item: Item, matricula: string): Promise<Item | undefined> {
  await wait();

  const response = await axios.post(`http://127.0.0.1:8000/api/checklists/checkitems/mod/`, {
    'id': item.id,
    'nombre': item.nombre,
    'activo': item.activo,
    'checklist': matricula,
  },{
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`
    }
  });

  const status = response.status;
  const data = response.data;
  
  if (status == 200){  
    try {
      if (typeof data === 'object'){
        return structuredClone(item);
      }
    } catch(error) {
      console.log("ERROR: ", error);
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
  }
}

export async function deleteItemService(itemId: number): Promise<number | undefined> {
  await wait();

  const response = await axios.post(`http://127.0.0.1:8000/api/checklists/checkitems/del/`, {
    'id': itemId,
  }, {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`
    }
  });

  const status = response.status;
  const data = response.data;
  
  if (status == 200){  
    try {
      if (typeof data === 'object'){
        return data['id'];
      }
    } catch(error) {
      console.log("ERROR: ", error);
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
  }
}
