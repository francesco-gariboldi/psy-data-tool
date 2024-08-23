import os
import rpy2
import r_warnings
import IPython

# Plot best models diagnostics
def plot_best_models_diagnostics(best_models, df_r):
    non_mixed_formula = best_models['non_mixed_best_model']['formula']
    mixed_formula = best_models['mixed_best_model']['formula']

    r_non_mixed_formula = rpy2.robjects.StrVector([non_mixed_formula])
    r_mixed_formula = rpy2.robjects.StrVector([mixed_formula])

    rpy2.robjects.globalenv['non_mixed_formula'] = r_non_mixed_formula[0]
    rpy2.robjects.globalenv['mixed_formula'] = r_mixed_formula[0]
    
    # Extract dependent variable from formula
    dependent_variable_non_mixed = non_mixed_formula.split('~')[0].strip()
    dependent_variable_mixed = mixed_formula.split('~')[0].strip()

    r_code = f"""
    non_mixed_model <- lm(non_mixed_formula, data=df_r)
    mixed_model <- lmer(mixed_formula, data=df_r)

    non_mixed_predictions <- predict(non_mixed_model, df_r)
    mixed_predictions <- predict(mixed_model, df_r, allow.new.levels = TRUE)

    pdf(file="./rplot.pdf", width = 7, height = 56)
    
    par(mfrow=c(10,1))
    # Diagnostic graphics for best non mixed model
    plot(non_mixed_model, which=1, main=sprintf("Non-Mixed Model: %s ", non_mixed_formula))
    plot(non_mixed_model, which=2, main=sprintf("Non-Mixed Model: %s ", non_mixed_formula))
    plot(non_mixed_model, which=3, main=sprintf("Non-Mixed Model: %s ", non_mixed_formula))
    plot(non_mixed_model, which=5, main=sprintf("Non-Mixed Model: %s ", non_mixed_formula))
    
    # Mixed Model diagnostic graphics using appropriate functions
    plot(fitted(mixed_model), resid(mixed_model), main=sprintf("Mixed Model: %s - Residuals vs Fitted", mixed_formula))
    qqnorm(resid(mixed_model), main=sprintf("Mixed Model: %s - Normal Q-Q", mixed_formula))
    qqline(resid(mixed_model))
    plot(fitted(mixed_model), sqrt(abs(resid(mixed_model))), main=sprintf("Mixed Model: %s - Scale-Location", mixed_formula))
    plot(hatvalues(mixed_model), resid(mixed_model), main=sprintf("Mixed Model: %s - Residuals vs Leverage", mixed_formula))
    
    # Prediction checks with performance::check_predictions
    check_predictions(non_mixed_model)
    check_predictions(mixed_model)
    
    dev.off()
    """
    
    try:
        rpy2.robjects.r(r_code)
        
        # Display the PDF file in the Jupyter notebook
        pdf_path = './rplot.pdf'
        display(IPython.display.IFrame(pdf_path, width=800, height=600))
    except Exception as e:
        print("Error encountered while generating plots:", e)
        r_warnings.print_r_warnings()


# Plot best models performance
def plot_best_models_performance(best_models, df_r):
    non_mixed_formula = best_models['non_mixed_best_model']['formula']
    mixed_formula = best_models['mixed_best_model']['formula']

    r_non_mixed_formula = rpy2.robjects.StrVector([non_mixed_formula])
    r_mixed_formula = rpy2.robjects.StrVector([mixed_formula])

    rpy2.robjects.globalenv['non_mixed_formula'] = r_non_mixed_formula[0]
    rpy2.robjects.globalenv['mixed_formula'] = r_mixed_formula[0]

    # Extract dependent variable from formula
    dependent_variable_non_mixed = non_mixed_formula.split('~')[0].strip()
    dependent_variable_mixed = mixed_formula.split('~')[0].strip()

# In the notebook, plots are published as the output of the cell:
# %R plot(X, Y)  # if you want R graphs to be in cell output ()
    
    r_code = f"""
    if (!requireNamespace("performance", quietly = TRUE)) {{
        install.packages("performance")
    }}

    print("Fitting non-mixed model...")
    non_mixed_model <- lm(non_mixed_formula, data=df_r)
    print("Fitting mixed model...")
    mixed_model <- lmer(mixed_formula, data=df_r)

    print("Generating predictions...")
    non_mixed_predictions <- predict(non_mixed_model, df_r)
    mixed_predictions <- predict(mixed_model, df_r, allow.new.levels = TRUE)

    print("Starting PDF device...")
    pdf(file="./rplot.pdf", width = 7, height = 32)
    
    par(mfrow=c(2,1))
    # Diagnostic graphics for best non mixed model using check_model
    print("Plotting non-mixed model diagnostics...")
    check_model(non_mixed_model, title = sprintf("Non-Mixed Model: %s", non_mixed_formula))
    
    # Diagnostic graphics for best mixed model using check_model
    print("Plotting mixed model diagnostics...")
    check_model(mixed_model, title = sprintf("Mixed Model: %s", mixed_formula))

    # Predictions check
    stack(simulate(non_mixed_model, 50 ))
    stack(simulate(mixed_model, 50 ))

    dev.off()
    print("PDF generation complete.")
    """

    try:
        rpy2.robjects.r(r_code)
        
        
        if os.path.exists(pdf_path):
            display(IPython.display.IFrame(pdf_path, width=800, height=600))
        else:
            print("PDF file was not created. Please check for errors in the R code.")
    except Exception as e:
        print("Error encountered while generating plots:", e)
        r_warnings.print_r_warnings()
       