from website import create_app 


app = create_app()

if __name__ == '__main__':#it means only if you run this file that the next line of code will be executed
    app.run(debug=True)#runs our web server. the "debug= true" just means any change to our code will make it automatically make it re-run
    
    #the above code is just the basic procedure for setting up the web server<!DOCTYPE html>

    