%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REGLA 1: Dos casillas negras no pueden estar juntas (sin contar diagonales)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Definimos que dos casillas son adyacentes si abs(c1-c2) + abs(r1 - r2) == 1
adj(C,R,C1,R1) :- col(C), col(C1), row(R), row(R1), |(C-C1)|+|(R-R1)|==1.

% Restringimos que las casillas negras no sean adyacentes
:- adj(C,R,C1,R), black(C,R), black(C1,R), C!=C1.
:- adj(C,R,C,R1), black(C,R), black(C,R1), R!=R1.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REGLA 2: Todas las casillas blancas deben estar interconectadas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Definimos como casilla blanca a la que no es negra
white(C,R) :- not black(C,R), col(C), row(R).

% Dos casillas blancas están conectadas si existe un "camino" de casillas blancas adyacentes
connected(C,R,C1,R1) :- adj(C,R,C1,R1), white(C,R), white(C1,R1).
connected(C,R,X,Y) :- connected(C1,R1,X,Y), adj(C,R,C1,R1), white(C,R), col(X), row(Y).

% Restringimos que las casillas blancas tienen que estar siempre conectadas
:- not connected(C,R,C1,R1), white(C,R), white(C1,R1), col(C), col(C1), row(R), row(R1), C!=C1, R!=R1.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REGLA 3: Cada habitación debe tener N casillas negras (Siempre que N > 0)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Definimos room_size como el tamaño y 2 esquinas opuestas de la habitación para facilitar la lectura del código
room_size(N,X1,Y1,X2,Y2) :- room(A,X1,Y1,X2,Y2), has(A,N).

% Restringimos que el número de casillas negras coincida con el especificado en la habitación 
N {black(C,R): col(C), row(R), C1<=C, C<=C2, R1<=R, R<=R2} N :- room_size(N,C1,R1,C2,R2), N>0.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REGLA 4: Las habitaciones con tamaño -1 se pueden rellenar como se quiera
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Especificamos que si la habitación tiene tamaño -1 no se restringe el número de casillas negras que puede tener
{black(C,R): col(C), row(R), C1<=C, C<=C2, R1<=R, R<=R2} :- room_size(-1,C1,R1,C2,R2).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REGLA 5: No puede haber un camino recto de casillas blancas que atraviese 3 o más habitaciones
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Definimos Inroom(X,Y,A) para especificar que la casilla (X,Y) está en la habitación A
inroom(X,Y,A) :- room(A,C,R,C1,R1), X<=C1, C<=X, Y<=R1, R<=Y, col(C), col(C1), col(X), row(Y), row(R1), row(R).

% Definimos el concepto de segmentos vertical y horizontal
segment(h;v).

% Definimos el concepto de path para las casillas blancas, S indica si el camino es horizontal o vertical, A continuación se especifica el origen
% y el destino y por último el número de habitaciones que ha atravesado ese camino
path(S,C,R,C,R,1) :- white(C,R), col(C), row(R), segment(S).

%%%%%%%%%%%%%%
% Horizontal
%%%%%%%%%%%%%%

% Si la casilla de al lado (C+1) pertenece a la misma habitación la añadimos al path sin más
path(h,C,R,C1,R,N) :- path(h,C+1,R,C1,R,N), adj(C,R,C+1,R), white(C,R), inroom(C,R,A), inroom(C+1,R,A), col(C;C1), row(R), num(N),N<3.

% Si la casilla de al lado (C+1) NO pertenece a la misma habitación la añadimos al path y sumamos 1 (para indicar que el path ahora atraviesa una habitación más)
path(h,C,R,C1,R,N+1) :- path(h,C+1,R,C1,R,N), adj(C,R,C+1,R), white(C,R), inroom(C,R,A), inroom(C+1,R,B), A!=B, col(C;C1), row(R), num(N), N<3.

%%%%%%%%%%%%%%
% Vertical
%%%%%%%%%%%%%%

% Si la casilla de debajo (R+1) pertenece a la misma habitación la añadimos al path sin más
path(v,C,R,C,R1,N) :- path(v,C,R+1,C,R1,N), adj(C,R,C,R+1), white(C,R), inroom(C,R,A), inroom(C,R+1,A), col(C), row(R;R1), num(N),N<3.

% Si la casilla de debajo (R+1) NO pertenece a la misma habitación la añadimos al path y sumamos 1 (para indicar que el path ahora atraviesa una habitación más)
path(v,C,R,C,R1,N+1) :- path(v,C,R+1,C,R1,N), adj(C,R,C,R+1), white(C,R), inroom(C,R,A), inroom(C,R+1,B), A!=B, col(C), row(R;R1), num(N), N<3.

% Descartamos los caminos rectos que atraviesen 3 habitaciones
:- path(S,C,R,X,Y,3), white(C,R), white(X,Y), col(C;X), row(R;Y), segment(S).

