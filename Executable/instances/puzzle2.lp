

% Indicamos el número de filas, columnas y habitaciones, yo lo dejo comentado porque esta información la añado desde python
% col(1..m). row(1..n). num(0..r-1).

room(0, 1, 6, 2, 6).
room(1, 3, 5, 4, 6).
room(2, 5, 5, 6, 6).
room(3, 1, 4, 2, 5).
room(4, 3, 4, 3, 4).
room(5, 4, 4, 4, 4).
room(6, 5, 2, 5, 4).
room(7, 6, 4, 6, 4).
room(8, 1, 2, 4, 3).
room(9, 6, 2, 6, 3).
room(10, 1, 1, 6, 1).

has(0, 0).
has(1, 0).
has(2, -1).
has(3, -1).
has(4, -1).
has(5, 1).
has(6, -1).
has(7, 0).
has(8, 1).
has(9, -1).
has(10, -1).