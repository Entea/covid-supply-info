class DonationResponse {
  final List<Donation> donations;

  DonationResponse(this.donations);

  factory DonationResponse.fromJson(dynamic json) {
    var donations = <Donation>[];
    for (var donationJson in json) {
      var donation = Donation.fromJson(donationJson);
      donations.add(donation);
    }
    return DonationResponse(donations);
  }
}

class Donation {
  final int id;
  final String donatorName;

  Donation(this.id, this.donatorName);

  factory Donation.fromJson(dynamic json) {
    return Donation(json['id'] as int, json['donator_name'] as String);
  }
}
