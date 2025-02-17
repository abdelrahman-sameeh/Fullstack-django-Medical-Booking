
def get_form_errors(form):
  error_messages = []
  for field, errors in form.errors.items():
    for error in errors:
        error_messages.append(f"{field}: {error}") 
  return error_messages