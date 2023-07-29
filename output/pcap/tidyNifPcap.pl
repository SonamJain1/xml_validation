#!/usr/bin/perl
#
## keep the disk space under control
## this is for a NIF
## looks at both insight pcap files and blockededr pcaps

tidy_pickup("/opt/engine/pcap/pickupSS7", 1);      # delete old files if get > 1G

# we get an "argument list too long" on Insight if there are more than 50,000 files in this dir
# # this can be resolved by changing the rsync command but then it will copy the .tmp files the IDS generates
# # until this is fixed, just keep the number of files down to below 50k

tidy_blockedpcap("/opt/engine/pcap/pickupSS7/blockedpcaps", 500);        # delete old files if more than 50,000
#tidy_blockedpcap("/home/engine/tidy/test_dir", 50000); # delete old files if more than 50,000

exit;

sub tidy_pickup
{
        my $pcapDir = shift;
        my $gb = shift;

        my $maxSize = $gb * 104857600;
        # get current size
        my @duOut = `du -b $pcapDir/*.pcap*`;

        my $size = 0;
        foreach my $f (@duOut)
        {
                $f =~ /^([0-9]+)/;
                $size += $1;
        }
        # now delete the oldest files if necessary
        if ($size > $maxSize)
        {
                opendir (D, $pcapDir);
                my @files = sort readdir D;
                close D;

                shift @files;
                shift @files;

                while ($size > $maxSize)
                {
                        my $file = shift @files;
                        print "deleting $file\n";

                        my $fileSize = (stat("$pcapDir/$file"))[7];
                        $size = ($size - $fileSize);

                        unlink "$pcapDir/$file";
                }
        }
}

sub tidy_blockedpcap
{
        my $pcapDir = shift;
        my $target_n_files = shift;
        # get current number of files in folder

        opendir (D, $pcapDir);
        my @files = sort readdir D;
        close D;

        shift @files;
        shift @files;

        my $size = scalar @files;

         # now delete the oldest files if necessary

        if ($size > $target_n_files)
        {
                while ($size > $target_n_files)
                {
                        my $file = shift @files;
                        print "deleting $file\n";

                        $size = ($size - 1);

                        unlink "$pcapDir/$file";
                }
        }
}
