from mpsh.database import db_session
from mpsh.models import MagicLink

db_session.add_all([
    MagicLink('mihajlakd@gmail.com', 'c6129e76-72e0-43bb-b8c3-93a7beb5a4cb'),
    MagicLink('turcinnadia2@gmail.com', 'c963deed-cebc-48ac-92e2-0c5af86f3237'),
    MagicLink('oksanaojops@ukr.net', '58af56b8-6f36-4dd4-b5c7-b56b2bc5d6f1'),
    MagicLink('dmytroipatiy@gmail.com', 'e9fff2cb-bd24-4bfb-bcc9-7f29a2339481'),
    MagicLink('petrobabiychuk@gmail.com', '67406088-15c5-46a1-9269-98c2439f81eb'),
    MagicLink('ira.irhuk@gmail.com', '1b98a492-b02f-49f4-953a-c472cddabfab'),
    MagicLink('jarynatynduk@gmail.com', '286b3c43-39c6-4ea5-8dce-0a97207d0982'),
    MagicLink('polyglot893@gmail.com', '31e14dcb-336e-44e2-a1de-57f198371ab7'),
    MagicLink('olenapryjma@gmail.com', '50b466e4-9cda-421a-9ad7-7385f9ad3134'),
    MagicLink('krisiscat10@gmail.com', '196d1c4a-a2d6-4492-b6f6-cfe00dd3a779'),
    MagicLink('martakondratik@gmail.com', '04737089-5d33-4417-af8d-dc825d1fa159')
])
db_session.commit()