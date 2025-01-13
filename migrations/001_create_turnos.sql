create table turnos (
  id uuid default uuid_generate_v4() primary key,
  nombre text not null,
  fecha_hora timestamp with time zone not null,
  confirmado boolean default false,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Función para actualizar updated_at
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- Trigger para updated_at
create trigger update_turnos_updated_at
    before update on turnos
    for each row
    execute function update_updated_at_column();

-- Habilitar realtime
alter table turnos replica identity full; 