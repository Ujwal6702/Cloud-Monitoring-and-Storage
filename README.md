# Cloud Monitoring and Storage

Combining ngrok with socket programming significantly enhances the efficiency and security of cloud systems. Ngrok's secure tunneling capability allows for remote monitoring and access to cloud resources without compromising internal networks, ensuring seamless management and proactive issue resolution in real-time. Socket programming complements this by facilitating real-time data retrieval and analysis between monitoring tools and cloud instances, optimizing data transfer and synchronization between clients and servers.

Additionally, using pyshark for packet sniffing enables the identification of websites visited by users, providing valuable insights that are securely transmitted to our server for comprehensive oversight. This approach ensures the company remains informed about user activities while maintaining data security. Socket programming further supports cloud storage by enabling secure data transfer to alternate servers, ensuring robust management and enhancing operational efficiency within cloud environments.


## How to run?

Please refer to the link and set up ngrok on your system by following the steps after signing up on ngrok.
   
<a> https://dashboard.ngrok.com/get-started/setup/windows </a>

## Cloud Storage System

1. Run ngrok by following the steps given under ngrok dashboad on a terminal.
2. Run `server.py` on of the system.
3. Run `client.py` on the other system. Make sure you have completed step 2 before this step.
4. Enter the details as shown under the prompt.
5. While entering the file name make sure the file is present on the same directory as the `client.py`.

## Cloud Monitoring System

1. Run ngrok by following the steps given under ngrok dashboad on a terminal.
2. Run `server.py` on of the system.
3. Run `client.py` on the other system. Make sure you have completed step 2 before this step.
4. Enter the details as shown under the prompt.
5. Now open any browser and start browsing through websites. You can find the website names being displayed on the server side.

