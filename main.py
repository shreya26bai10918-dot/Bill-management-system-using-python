from database import create_database
from gui import BillApp

create_database()

app = BillApp()
app.mainloop()