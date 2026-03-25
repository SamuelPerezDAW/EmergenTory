import type { Usuario, Vehiculo } from '@/types';

export const mockUser: Usuario = {
  id: 1,
  username: 'coordinador112',
  email: 'coordinador@emergentory.app',
  first_name: 'Lucia',
  last_name: 'Medina',
  perfil: {
    admin: true,
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=240&q=80',
    bio: 'Responsable de logística y control de material en la flota de emergencias.',
    telefono: '+34 600 100 112',
  },
};

export const mockVehiculos: Vehiculo[] = [
  {
    matricula: 'AMB-4201',
    marca: 'Mercedes-Benz',
    modelo: 'Sprinter 319',
    categoria: 'Ambulancia UVI',
    lista: {
      id: 201,
      creado: '2026-03-10T08:00:00Z',
      actualizado: '2026-03-25T07:30:00Z',
      items: [
        { id: 1, nombre: 'Desfibrilador', activo: true },
        { id: 2, nombre: 'Maletín de vía aérea', activo: true },
        { id: 3, nombre: 'Bombona de oxígeno reserva', activo: false },
      ],
    },
  },
  {
    matricula: 'BOM-1038',
    marca: 'MAN',
    modelo: 'TGM 18.320',
    categoria: 'Autobomba urbana',
    lista: {
      id: 202,
      creado: '2026-03-11T10:15:00Z',
      actualizado: '2026-03-24T21:10:00Z',
      items: [
        { id: 4, nombre: 'Manguera de ataque rápido', activo: true },
        { id: 5, nombre: 'Equipo ERA', activo: true },
        { id: 6, nombre: 'Cámara térmica', activo: true },
      ],
    },
  },
  {
    matricula: 'POL-7719',
    marca: 'Toyota',
    modelo: 'Land Cruiser',
    categoria: 'Unidad policial',
    lista: {
      id: 203,
      creado: '2026-03-09T12:40:00Z',
      actualizado: '2026-03-25T06:55:00Z',
      items: [
        { id: 7, nombre: 'Kit de balizamiento', activo: true },
        { id: 8, nombre: 'Tablet de incidencias', activo: false },
        { id: 9, nombre: 'Linterna táctica', activo: true },
      ],
    },
  },
];
