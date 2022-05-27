import os


class ScannerCommunication:
    """ Class methods for scanning web links that direct to files for viruses. """

    def get_virus_ratio(self, links) -> float:
        """
        Scans the given links' contents for viruses.

        Parameters:
            links (list): List of web links to the files to scan.

        Returns:
            float: Percentage of links that have been scanned for viruses.
        """

        # Initialize a counter for the number of infected links found
        infected_links = 0

        # Iterate through the links
        for link in links:
            # Scan the link
            if self.scan_link(link):
                # Increment the counter if a virus has been detected
                infected_links += 1

        # Return the percentage of links that have been scanned for viruses
        return infected_links / len(links)

    def scan_link(self, link) -> bool:
        """
        Scans the given link's contents for viruses.

        Parameters:
            link (str): Web link to the file to scan.

        Returns:
            bool: True if a virus has been detected, False otherwise.
        """

        # Open a command stream with the clamdscan command
        stream = os.popen(
            f'wget -qO- {link} | clamdscan --config-file=clamav/client_clamd.conf -')
        # Get the output of the scan
        feedback = stream.readlines()
        # Close the stream
        stream.close()

        # Extract the virus count from the output
        virus_count = feedback[3].strip().split(': ')[1]

        # Return True if a virus has been detected, False otherwise
        if virus_count == 0:
            return False
        else:
            return True
