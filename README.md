
gcloud builds submit --tag gcr.io/streamlit-app-419915/ipl2024_dream11 --project=streamlit-app-419915

gcloud run deploy --image gcr.io/streamlit-app-419915/ipl2024_dream11 --platform managed --project=streamlit-app-419915 --allow-unauthenticated