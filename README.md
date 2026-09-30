Week 4 homework deployment instructions

1. **Create secrets:**
Create a Secret named `week5` with the following keys
   - `DB_PASSWORD`
   - `MYSQL_ROOT_PASSWORD`
   - ` REST_COUNTRIES_API_KEY:`

2. **Apply Manifests:**
   In the Rahti Web Console, click the **+ (Import YAML)** button in the top navigation bar and apply the manifests in `/kubernetes` in numerical order:
   - `01-storage-config.yaml`
   - `02-secret.yaml`
   - `03-mysqql.yaml`
   - `04-backend.yaml`
   - `05-frontend.yaml`

4. **Access the App:**
   Navigate to **Networking** -> **Routes** and open the generated public URL for `frontend-route`.