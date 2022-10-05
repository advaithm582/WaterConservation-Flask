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

from flask import render_template, redirect, url_for, current_app, flash, request, abort
from flask_login import login_required, current_user
from markdown import markdown

from app import db
from app.models import AMSDCApp
from app.amsdcapps import bp
from app.amsdcapps.forms import AppAddingForm, AppEditingForm


def index():
    """determine_home [summary]

    Returns:
        str: Response
    """
    return redirect("https://amsdc.github.io/products")


@login_required
def add():
    form = AppAddingForm()
    
    if form.validate_on_submit():
        wc = AMSDCApp(
            uniqname = form.uniqname.data,
            name = form.name.data,
            released = form.released.data,
            lastupdated = form.lastupdated.data,
            latestver = form.latestver.data,
            license = form.license.data,
            programming_lang = form.programming_lang.data,
            lang = form.lang.data,
            type = form.type.data,
            copyright = form.copyright.data,
            repository = form.repository.data,
            installer = form.installer.data,
            shortdesc = form.shortdesc.data,
            longdesc = form.longdesc.data
        )
        db.session.add(wc)
        db.session.commit()
        flash("Added report successfully!")
        return redirect(url_for("amsdcapps.add"))
    
    return render_template("amsdcapps/new.html",
                           form=form)
    

@login_required
def edit():
    data = AMSDCApp.query.filter_by(uniqname=request.args["productID"]).first_or_404()

    form = AppEditingForm(obj=data)
    
    if form.validate_on_submit():
        # data.uniqname = form.uniqname.data
        data.name = form.name.data
        data.released = form.released.data
        data.lastupdated = form.lastupdated.data
        data.latestver = form.latestver.data
        data.license = form.license.data
        data.programming_lang = form.programming_lang.data
        data.lang = form.lang.data
        data.type = form.type.data
        data.copyright = form.copyright.data
        data.repository = form.repository.data
        data.installer = form.installer.data
        data.shortdesc = form.shortdesc.data
        data.longdesc = form.longdesc.data
        #db.session.add(wc)
        db.session.commit()
        flash("Edited report successfully!")
        return redirect(url_for("amsdcapps.edit", productID=request.args["productID"]))
    
    return render_template("amsdcapps/new.html",
                           form=form)


    
def getsoft():
    if "productID" in request.args:
        data = AMSDCApp.query.filter_by(uniqname=request.args["productID"]).first()
        if data:
            ldhtm = markdown(data.longdesc)
            return render_template("amsdcapps/softdetails.html", data=data, ldhtm=ldhtm)
        else:
            abort(400)
    else:
        abort(400)
