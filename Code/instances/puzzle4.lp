
% Indicamos el número de filas, columnas y habitaciones, yo lo dejo comentado porque esta información la añado desde python
% col(1..m). row(1..n). num(0..r-1).

room(0,1,1,4,1).
room(1,1,2,3,3).
room(2,1,4,3,4).
room(3,1,5,3,6).
room(4,5,1,6,2).
room(5,4,2,4,2).
room(6,4,3,5,4).
room(7,6,3,6,4).
room(8,4,5,6,6).

has(0,2).
has(1,1).
has(2,2).
has(3,2).
has(4,0).
has(5,-1).
has(6,0).
has(7,-1).
has(8,2).