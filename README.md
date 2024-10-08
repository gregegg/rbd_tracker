# Purpose
Explore raw data from [Oura Ring](https://ouraring.com/) for potential use in tracking RBD events.

## Initial Scope
Extract count of large movements during periods of sleep classifed as "REM".

Unverified Assumption: 
- Sleep stage classification isn't thrown off by RBD events

## Future Scope


# Docs

## Technical
- Oura V2 API [Docs](https://cloud.ouraring.com/v2/docs)
- "Multiple Sleep Documents" [API](https://cloud.ouraring.com/v2/docs#operation/Single_session_Document_v2_usercollection_session__document_id__get)

## Literature
- Svensson, 2024 [Sleep Medicine, Volume 115, March 2024, Pages 251-263](https://www.sciencedirect.com/science/article/pii/S1389945724000200)
    - The Oura Ring did not significantly differ from PSG for the measures time in bed, total sleep time, sleep onset latency, sleep period time, wake after sleep onset, time spent in light sleep, and time spent in deep sleep. 
- Altini, 2021 [Sensors 2021, 21, 4302](https://www.mdpi.com/1424-8220/21/13/4302)
   - Personal observation:  From Figs 11,12 - Accelerometer data by itself is not able to predict the sleep stage.  It takes a combination of accelerometer, heart rate, temperature and circadian info.  It's plausible, then, that when the Oura Algorithm classifies a sleep stage as "REM", the stage classification may not be affected by a RBD event.
- Kinnunen, 2016 [self-published?](https://ouraring.com/blog/wp-content/uploads/2018/10/Validity-of-the-OURA-Ring-in-determining-Sleep-Quantity-and-Quality-2016.pdf)
    


# Developer

## Package management 

Python package management is performed with conda environments.  

1. Ensure that you have installed `conda` (e.g., from https://github.com/conda-forge/miniforge/releases)
2. Create your local python environment by running  `conda create -n rbd_dev --file requirements.txt` in your terminal
3. Optional (if using vscode):  update PYTHONPATH in `.vscode/settings.json` to point to your local enviroment

## API Key

1. Log into https://cloud.ouraring.com/personal-access-tokens and create a personal access token.  Make sure to copy this key immediately.
2. Create a text file named `.env` in your project root. Add the following line to it, replacing 'abc123' with the personal access token.
```
API_KEY=abc123 
```

## Execution

After setting up your API key, execute `dvc repro` from the terminal to run the analysis pipeline.

(See [dvc documentation](https://dvc.org/doc/start) for more info)
