# This file is part of MyPHP.

# MyPHP is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free 
# Software Foundation, either version 3 of the License, or (at your 
# option) any later version.

# MyPHP is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.

# You should have received a copy of the GNU General Public License along
# with MyPHP. If not, see <https://www.gnu.org/licenses/>. 

from app.amsdcapps import bp
from app.amsdcapps import views as v


bp.add_url_rule("/", view_func=v.index)
bp.add_url_rule("/software/management/addSoftware.aspx", view_func=v.add, methods=['GET', 'POST'])
bp.add_url_rule("/software/management/editSoftware.aspx", view_func=v.edit, methods=['GET', 'POST'])
# bp.add_url_rule("/leaderboard", view_func=v.leaderboard)
bp.add_url_rule("/software/getDetails", view_func=v.getsoft)