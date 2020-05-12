FROM freeradius/freeradius-server:3.0.19

COPY ./configs/sql /etc/freeradius/mods-available/sql
COPY ./configs/queries.conf /etc/freeradius/mods-config/sql/main/postgresql/queries.conf

RUN ln -s /etc/freeradius/mods-available/sql /etc/freeradius/mods-enabled/sql