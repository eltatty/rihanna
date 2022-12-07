async function loadTables() {
    const response = await fetch("http://localhost:5000/servers");
    const data = await response.json();

    for (const version of data) {

        const versionElement = document.createElement('h1');

        versionElement.textContent = version[0]['Version'];

        document.getElementById('mainDiv').appendChild(versionElement);

        const tableElement = document.createElement('table');

        const theadElement = document.createElement('thead');

        const theadRowElement = document.createElement('tr');

        const h2Name = document.createElement('h2');
        const h2Interfaces = document.createElement('h2');
        const h2BuildInfo = document.createElement('h2');
        const h2Actions = document.createElement('h2');
        const h2Client = document.createElement('h2');

        h2Name.textContent = 'Name';
        h2Interfaces.textContent = 'Interfaces';
        h2BuildInfo.textContent = 'Build Info';
        h2Actions.textContent = 'Actions';
        h2Client.textContent = 'Client';

        const thName = document.createElement('th');
        const thInterfaces = document.createElement('th');
        const thBuildInfo = document.createElement('th');
        const thActions = document.createElement('th');
        const thClient = document.createElement('th');

        thName.appendChild(h2Name);
        thInterfaces.appendChild(h2Interfaces);
        thBuildInfo.appendChild(h2BuildInfo);
        thActions.appendChild(h2Actions);
        thClient.appendChild(h2Client);

        theadRowElement.appendChild(thName);
        theadRowElement.appendChild(thInterfaces);
        theadRowElement.appendChild(thBuildInfo);
        theadRowElement.appendChild(thActions);
        theadRowElement.appendChild(thClient);


        theadElement.appendChild(theadRowElement);
        tableElement.appendChild(theadElement);

        const tbodyElement = document.createElement('tbody');

        for(const server of version){
            const tbodyRowElement = document.createElement('tr');

            // Name
            const tdName = document.createElement('td');
            const h3Name = document.createElement('h3');
            h3Name.textContent = server['Name'];
            tdName.appendChild(h3Name);

            tbodyRowElement.appendChild(tdName);

            // Interfaces (don`t forget to create respective links in the href attributes)
            const tdInterface = document.createElement('td');

            const h3SPDRM = document.createElement('h3');
            const h3ADMIN = document.createElement('h3');
            const h3HOST = document.createElement('h3');

            h3SPDRM.textContent = 'SPDRM ' + server['Ws Port'];
            h3ADMIN.textContent = 'ADMIN ' + server['Admin Port'];
            h3HOST.textContent = 'HOST ' + server['Hostname'];

            const pSPDRM = document.createElement('p');
            const pADMIN = document.createElement('p');
            const pHOST = document.createElement('p');

            pSPDRM.appendChild(h3SPDRM);
            pADMIN.appendChild(h3ADMIN);
            pHOST.appendChild(h3HOST);
            
            const aSPDRM = document.createElement('a');
            const aADMIN = document.createElement('a');

            aSPDRM.appendChild(pSPDRM);
            aADMIN.appendChild(pADMIN);

            tdInterface.appendChild(aSPDRM);
            tdInterface.appendChild(aADMIN);
            tdInterface.appendChild(pHOST);

            tbodyRowElement.appendChild(tdInterface);

            // Build Info
            const tdBuildInfo = document.createElement('td');
            
            const h3Version = document.createElement('h3');
            const h3BuildDate = document.createElement('h3'); 
            const h3PE = document.createElement('h3');
            const h3DM = document.createElement('h3');
            const h3KB = document.createElement('h3');

            h3Version.textContent = 'Version ' + server['Version'];
            h3BuildDate.textContent = 'Build Date ' + server['build_date'];
            h3PE.textContent = 'Process Enabled ' + server['process_enabled'];
            h3DM.textContent = 'DM Enabled ' + server['dm_enabled'];
            h3KB.textContent = 'KB Enabled ' + server['kb_enabled'];

            console.log(server);
            typeof server['kb_enabled']

            const pVersion = document.createElement('p');
            const pBuildDate = document.createElement('p');
            const pPE = document.createElement('p');
            const pDM = document.createElement('p');
            const pKB = document.createElement('p');

            pVersion.appendChild(h3Version);
            pBuildDate.appendChild(h3BuildDate);
            pPE.appendChild(h3PE);
            pDM.appendChild(h3DM);
            pKB.appendChild(h3KB);

            tdBuildInfo.appendChild(pVersion);
            tdBuildInfo.appendChild(pBuildDate);
            tdBuildInfo.appendChild(pPE);
            tdBuildInfo.appendChild(pDM);
            tdBuildInfo.appendChild(pKB);

            tbodyRowElement.appendChild(tdBuildInfo);

            
            // Attach Row to Body to Document
            tbodyElement.appendChild(tbodyRowElement);
            tableElement.appendChild(tbodyElement);
            document.getElementById('mainDiv').appendChild(tableElement);
        }

    }
}